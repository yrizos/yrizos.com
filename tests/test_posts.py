from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from bs4 import BeautifulSoup

from scripts.posts import cli as cli_mod
from scripts.posts import fetch_devto as devto_mod
from scripts.posts import fetch_medium as medium_mod
from scripts.posts.blog_post import BlogPost


class FakeEntry(dict):
    __getattr__ = dict.__getitem__


def test_blog_post_defaults() -> None:
    entry = BlogPost(
        title="Example",
        slug="example",
        date=datetime(2024, 1, 2, tzinfo=timezone.utc),
        original_url="https://example.com",
        markdown_body="# Hello",
    )

    assert entry.tags == []
    assert entry.image_url is None
    assert entry.image_alt == ""
    assert entry.series_title is None
    assert entry.series_order is None


def test_cli_helpers_and_front_matter() -> None:
    assert cli_mod.slugify("Hello, World! 2024") == "hello-world-2024"
    assert cli_mod.clean_url("https://example.com/path?x=1#frag") == "https://example.com/path"

    date = cli_mod.parse_publish_date("Mon, 01 Jan 2024 00:00:00 +0000", None, "Example")
    assert date == datetime(2024, 1, 1, tzinfo=timezone.utc)

    post = BlogPost(
        title="Example title",
        slug="example-title",
        date=datetime(2024, 1, 2, tzinfo=timezone.utc),
        original_url="https://example.com/post",
        markdown_body="body",
        tags=["python", "testing"],
        image_url="https://example.com/cover.png",
        image_alt="Cover photo",
        series_title="Series Title",
        series_order=3,
    )

    front_matter = cli_mod.build_front_matter(post, Path("images/writing/example-title.png"))
    assert "title = \"Example title\"" in front_matter
    assert 'tags = ["python", "testing"]' in front_matter
    assert 'series_title = "Series Title"' in front_matter
    assert 'series_order = 3' in front_matter

    assert cli_mod.to_toml_value(True) == "true"
    assert cli_mod.to_toml_value(datetime(2024, 1, 2, tzinfo=timezone.utc)) == "2024-01-02T00:00:00+00:00"
    assert cli_mod.determine_image_filename("hello", "https://example.com/cover.jpeg") == "hello.jpeg"


def test_cli_download_and_write_post(monkeypatch, tmp_path: Path) -> None:
    class FakeResponse:
        content = b"image-bytes"

        def raise_for_status(self) -> None:
            return None

    class FakeSession:
        def __init__(self) -> None:
            self.headers = {}

        def update(self, headers) -> None:
            self.headers.update(headers)

        def get(self, url, timeout):
            assert url == "https://example.com/cover.png"
            assert timeout == 30
            return FakeResponse()

    monkeypatch.setattr(cli_mod.requests, "Session", FakeSession)
    monkeypatch.setattr(cli_mod, "POSTS_DIR", tmp_path / "posts")
    monkeypatch.setattr(cli_mod, "IMAGES_DIR", tmp_path / "images")
    monkeypatch.setattr(cli_mod, "WEB_IMAGE_PREFIX", Path("images/writing"))

    post = BlogPost(
        title="Example",
        slug="example",
        date=datetime(2024, 1, 2, tzinfo=timezone.utc),
        original_url="https://example.com/post",
        markdown_body="# Header\n\ntext",
        image_url="https://example.com/cover.png",
        image_alt="Example cover",
    )

    cli_mod.write_post(post)

    assert (tmp_path / "images" / "example.png").exists()
    assert (tmp_path / "posts" / "example.md").exists()
    rendered = (tmp_path / "posts" / "example.md").read_text(encoding="utf-8")
    assert "image = \"images/writing/example.png\"" in rendered
    assert "# Header" in rendered


def test_cli_prompt_and_process_posts(monkeypatch) -> None:
    captured = []

    responses = iter(["yes", "no", "exit"])
    monkeypatch.setattr(cli_mod.console, "input", lambda *_args, **_kwargs: next(responses))

    post = BlogPost(
        title="One",
        slug="one",
        date=datetime(2024, 1, 2, tzinfo=timezone.utc),
        original_url="https://example.com/1",
        markdown_body="body",
    )
    assert cli_mod.prompt_for_post(post) == "yes"
    assert cli_mod.prompt_for_post(post) == "no"
    assert cli_mod.prompt_for_post(post) == "exit"

    def fake_write(post_obj):
        captured.append(post_obj.title)

    monkeypatch.setattr(cli_mod, "write_post", fake_write)
    monkeypatch.setattr(cli_mod.console, "input", lambda *_args, **_kwargs: "yes")
    cli_mod.process_posts([post])
    assert captured == ["One"]


def test_medium_helpers_extract_and_parse() -> None:
    soup = BeautifulSoup(
        """
        <article>
            <h1>Initial heading</h1>
            <p>Originally published at <a href="https://example.com/original">story</a> on January 2, 2024</p>
            <img src="https://tracking.medium.com/_/stat" alt="tracking">
            <img src="https://cdn.example.com/cover.jpg" alt="cover image">
        </article>
        """,
        "html.parser",
    )

    medium_mod.normalize_headings(soup)
    assert soup.find("h2").text.strip() == "Initial heading"

    image_url, image_alt = medium_mod.pop_first_image(soup)
    assert image_url == "https://cdn.example.com/cover.jpg"
    assert image_alt == "cover image"

    original_url, original_date = medium_mod.extract_original_metadata(soup)
    assert original_url == "https://example.com/original"
    assert original_date == datetime(2024, 1, 2, tzinfo=timezone.utc)

    tracking_soup = BeautifulSoup('<img src="https://tracking.medium.com/_/stat"><img src="https://cdn.example.com/x.jpg">', "html.parser")
    medium_mod.remove_tracking_images(tracking_soup)
    assert tracking_soup.find("img")["src"] == "https://cdn.example.com/x.jpg"

    tags = medium_mod.extract_tags({"tags": [{"term": "python"}, {"term": "testing"}, {"term": "python"}]})
    assert tags == ["python", "testing"]

    assert medium_mod.is_tracking_image("https://tracking.medium.com/_/stat") is True
    assert medium_mod.is_tracking_image("https://cdn.example.com/x.jpg") is False

    entry = FakeEntry(
        {
            "title": "A Great Post",
            "published": "Mon, 01 Jan 2024 00:00:00 +0000",
            "link": "https://example.com/post",
            "content": [FakeEntry({"value": '<article><h1>Heading</h1><p>Hello world.</p><p>Originally published at <a href="https://example.com/original">story</a> on January 2, 2024</p><img src="https://cdn.example.com/cover.jpg" alt="Cover"></article>'})],
            "tags": [{"term": "python"}, {"term": "testing"}],
        }
    )

    post = medium_mod.parse_medium_entry(entry)
    assert post.slug == "a-great-post"
    assert post.original_url == "https://example.com/original"
    assert post.image_url == "https://cdn.example.com/cover.jpg"
    assert post.tags == ["python", "testing"]


def test_fetch_medium_posts_uses_feedparser(monkeypatch) -> None:
    entry = FakeEntry({
        "title": "Medium post",
        "published": "Mon, 01 Jan 2024 00:00:00 +0000",
        "link": "https://example.com/post",
        "content": [FakeEntry({"value": '<article><h1>Title</h1><p>Post text.</p></article>'})],
    })

    class FeedResult:
        bozo = False
        entries = [entry]

    monkeypatch.setattr(medium_mod.feedparser, "parse", lambda _url: FeedResult())
    posts = medium_mod.fetch_medium_posts("https://example.com/feed")
    assert len(posts) == 1
    assert posts[0].title == "Medium post"


def test_devto_article_helpers(monkeypatch) -> None:
    assert devto_mod.extract_devto_article_id("https://dev.to/user/example-title-123") == "user/example-title-123"
    assert devto_mod.extract_devto_article_id("https://dev.to/user") is None
    assert devto_mod.extract_devto_slug({"link": "https://dev.to/user/example-title-123"}) == "example-title-123"
    assert devto_mod.extract_tags({"tags": [{"term": "python"}, {"term": "python"}, {"term": "writing"}]}) == ["python", "writing"]

    class FakeResponse:
        text = "<html><head><title>Testing Series Articles - DEV Community</title></head></html>"

        def raise_for_status(self) -> None:
            return None

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(devto_mod.requests, "get", fake_get)
    assert devto_mod.fetch_series_title("user", 42) == "Testing"

    def fake_list_get(url, timeout):
        class Response:
            def raise_for_status(self) -> None:
                return None

            def json(self):
                return [{"id": 9, "collection_id": 42, "published_at": "2023-01-01T00:00:00Z"}, {"id": 10, "collection_id": 42, "published_at": "2023-01-02T00:00:00Z"}]

        return Response()

    monkeypatch.setattr(devto_mod.requests, "get", fake_list_get)
    assert devto_mod.calculate_series_order("user", 42, 10) == 2


def test_parse_devto_entry_and_feed(monkeypatch) -> None:
    entry = FakeEntry(
        {
            "title": "Dev post",
            "published": "Mon, 01 Jan 2024 00:00:00 +0000",
            "link": "https://dev.to/author/dev-post-123",
            "tags": [{"term": "python"}],
        }
    )

    monkeypatch.setattr(devto_mod, "fetch_devto_article", lambda article_id: {
        "body_markdown": "# Heading\n\nContent",
        "cover_image": "https://cdn.example.com/dev-cover.jpg",
        "title": "Dev post",
        "tag_list": ["python", "writing"],
        "collection_id": None,
    })
    post = devto_mod.parse_devto_entry(entry)
    assert post.slug == "dev-post"
    assert post.image_url == "https://cdn.example.com/dev-cover.jpg"
    assert post.tags == ["python", "writing"]

    class FeedResult:
        bozo = False
        entries = [entry]

    monkeypatch.setattr(devto_mod.feedparser, "parse", lambda _url: FeedResult())
    posts = devto_mod.fetch_devto_posts("https://dev.to/feed")
    assert len(posts) == 1
    assert posts[0].title == "Dev post"

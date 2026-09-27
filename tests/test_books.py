from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from scripts import fetch_books as fetch_books_mod
from scripts import fetch_reading as fetch_reading_mod
from scripts import goodreads as goodreads_mod


class FakeEntry(dict):
    __getattr__ = dict.__getitem__


def test_fetch_books_helpers(monkeypatch) -> None:
    assert fetch_books_mod.slugify("Hello, World!") == "hello-world"
    assert fetch_books_mod.determine_image_filename("my-book", "https://example.com/img.png") == "my-book.png"
    assert fetch_books_mod.to_toml_value(["a", "b"]) == '["a", "b"]'

    book = fetch_books_mod.Book(
        title="Clean Code",
        author="Robert Martin",
        slug="clean-code",
        goodreads_url="https://www.goodreads.com/book/show/1",
        book_id="1",
        isbn="9780132350884",
        rating="5",
        date_read="2024-01-01",
        image_url="https://example.com/cover.jpg",
        tags=["software"],
    )

    front = fetch_books_mod.build_front_matter(book, "images/books/recommendations/clean-code.jpg")
    assert 'title = "Clean Code"' in front
    assert 'goodreads_url = "https://www.goodreads.com/book/show/1"' in front
    assert 'tags = ["software"]' in front

    def fake_head(url, timeout):
        class Response:
            status_code = 200

        return Response()

    monkeypatch.setattr(fetch_books_mod.requests, "head", fake_head)
    assert fetch_books_mod.get_image_url_from_sources("1", "9780132350884", "Clean Code", "Robert Martin") == "https://covers.openlibrary.org/b/isbn/9780132350884-L.jpg"

    class FakeResponse:
        status_code = 200

        def json(self):
            return {"items": [{"volumeInfo": {"imageLinks": {"extraLarge": "https://books.google.com/cover.jpg"}}}]}

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(fetch_books_mod.requests, "get", fake_get)
    assert fetch_books_mod.get_image_url_from_sources("1", "", "Clean Code", "Robert Martin") == "https://books.google.com/cover.jpg"


def test_fetch_books_feed_and_process(monkeypatch, tmp_path: Path) -> None:
    entry = FakeEntry(
        {
            "book_id": "123",
            "user_rating": "5",
            "title": "The Pragmatic Programmer",
            "author_name": "Andrew Hunt",
            "isbn": "9780201616224",
            "link": "https://www.goodreads.com/book/show/123?utm_medium=api&utm_source=rss",
            "user_read_at": "Tue, 02 Jan 2024 12:00:00 +0000",
            "book_large_image_url": "https://example.com/book.jpg",
            "user_shelves": "favorites, software, engineering",
        }
    )

    class FeedResult:
        bozo = False
        entries = [entry]

    monkeypatch.setattr(fetch_books_mod.feedparser, "parse", lambda _url: FeedResult())
    books = fetch_books_mod.fetch_goodreads_books()
    assert len(books) == 1
    assert books[0].goodreads_url == "https://www.goodreads.com/book/show/123"
    assert books[0].date_read == "2024-01-02"
    assert books[0].tags == ["software", "engineering"]

    monkeypatch.setattr(fetch_books_mod, "BOOKS_DIR", tmp_path / "books")
    monkeypatch.setattr(fetch_books_mod, "IMAGES_DIR", tmp_path / "images")
    monkeypatch.setattr(fetch_books_mod, "download_image", lambda url, destination: destination.write_bytes(b"img"))

    success, action = fetch_books_mod.process_book(books[0])
    assert success is True
    assert action in {"created", "updated"}
    assert (tmp_path / "books" / "the-pragmatic-programmer-andrew-hunt.md").exists()

    monkeypatch.setattr(fetch_books_mod, "BOOKS_DIR", tmp_path / "books")
    monkeypatch.setattr(fetch_books_mod, "IMAGES_DIR", tmp_path / "images")
    title_file = tmp_path / "books" / "skip-book.md"
    title_file.write_text('book_id = "29630264"\nimage = "images/books/recommendations/skip.jpg"\ntitle = "Skip Me"\n', encoding="utf-8")
    fetch_books_mod.remove_skipped_books()
    assert not title_file.exists()


def test_get_image_url_from_sources_falls_through_in_order(monkeypatch) -> None:
    calls = []

    def fake_head(url, timeout):
        calls.append(("head", url))

        class Response:
            status_code = 404  # no direct ISBN cover

        return Response()

    def fake_get(url, timeout):
        calls.append(("get", url))

        class Response:
            status_code = 200

            def json(self):
                if "googleapis" in url:
                    return {"items": []}  # Google Books has nothing for either query
                return {"docs": [{"cover_i": 12345}]}  # Open Library search hits

        return Response()

    monkeypatch.setattr(goodreads_mod.requests, "head", fake_head)
    monkeypatch.setattr(goodreads_mod.requests, "get", fake_get)

    result = goodreads_mod.get_image_url_from_sources(
        "1", "9780132350884", "Clean Code", "Robert Martin"
    )

    assert result == "https://covers.openlibrary.org/b/id/12345-L.jpg"
    assert [kind for kind, _ in calls] == ["head", "get", "get", "get"]
    assert "covers.openlibrary.org/b/isbn" in calls[0][1]
    assert "isbn:" in calls[1][1]
    assert "isbn:" not in calls[2][1]
    assert "openlibrary.org/search.json" in calls[3][1]


def test_remove_duplicate_books_keeps_shared_image(monkeypatch, tmp_path: Path) -> None:
    books_dir = tmp_path / "books"
    images_dir = tmp_path / "images"
    books_dir.mkdir()
    images_dir.mkdir()

    shared_image = images_dir / "shared.jpg"
    shared_image.write_bytes(b"cover")
    unique_image = images_dir / "unique.jpg"
    unique_image.write_bytes(b"cover2")

    (books_dir / "keep.md").write_text(
        'book_id = "1"\nimage = "images/books/recommendations/shared.jpg"\n'
        'title = "The Pragmatic Programmer: A Journey"\n',
        encoding="utf-8",
    )
    (books_dir / "same-image-duplicate.md").write_text(
        'book_id = "1"\nimage = "images/books/recommendations/shared.jpg"\n'
        'title = "The Pragmatic Programmer"\n',
        encoding="utf-8",
    )
    (books_dir / "different-image-duplicate.md").write_text(
        'book_id = "1"\nimage = "images/books/recommendations/unique.jpg"\n'
        'title = "Pragmatic Prog"\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(fetch_books_mod, "BOOKS_DIR", books_dir)
    monkeypatch.setattr(fetch_books_mod, "IMAGES_DIR", images_dir)

    fetch_books_mod.remove_duplicate_books()

    assert (books_dir / "keep.md").exists()
    assert not (books_dir / "same-image-duplicate.md").exists()
    assert not (books_dir / "different-image-duplicate.md").exists()
    assert shared_image.exists()
    assert not unique_image.exists()


def test_fetch_reading_helpers(monkeypatch) -> None:
    assert fetch_reading_mod.slugify("Now Reading!") == "now-reading"
    assert fetch_reading_mod.determine_image_filename("my-book", "https://example.com/image.webp") == "my-book.webp"
    assert fetch_reading_mod.to_toml_value(False) == "false"

    book = fetch_reading_mod.Book(
        title="Dune",
        author="Frank Herbert",
        slug="dune",
        goodreads_url="https://www.goodreads.com/book/show/2",
        book_id="2",
        isbn="9780441172719",
        image_url="https://example.com/dune.jpg",
        date_added="2024-01-03",
    )

    front = fetch_reading_mod.build_front_matter(book, "images/books/currently-reading/dune.jpg")
    assert 'title = "Dune"' in front
    assert 'date = "2024-01-03"' in front

    class Response:
        status_code = 200

        def json(self):
            return {"items": [{"volumeInfo": {"imageLinks": {"large": "https://books.google.com/dune.jpg"}}}]}

    monkeypatch.setattr(fetch_reading_mod.requests, "get", lambda url, timeout: Response())
    assert fetch_reading_mod.get_image_url_from_sources("2", "", "Dune", "Frank Herbert") == "https://books.google.com/dune.jpg"


def test_fetch_reading_feed_and_process(monkeypatch, tmp_path: Path) -> None:
    entry = FakeEntry(
        {
            "book_id": "456",
            "title": "Atomic Habits",
            "author_name": "James Clear",
            "isbn": "9780735211292",
            "link": "https://www.goodreads.com/book/show/456?utm_medium=api&utm_source=rss",
            "book_large_image_url": "https://example.com/atomic.jpg",
            "user_date_added": "Wed, 03 Jan 2024 09:00:00 +0000",
        }
    )

    class FeedResult:
        bozo = False
        entries = [entry]

    monkeypatch.setattr(fetch_reading_mod.feedparser, "parse", lambda _url: FeedResult())
    books = fetch_reading_mod.fetch_goodreads_books()
    assert len(books) == 1
    assert books[0].date_added == "2024-01-03"
    assert books[0].goodreads_url == "https://www.goodreads.com/book/show/456"

    monkeypatch.setattr(fetch_reading_mod, "BOOKS_DIR", tmp_path / "reading")
    monkeypatch.setattr(fetch_reading_mod, "IMAGES_DIR", tmp_path / "reading-images")
    monkeypatch.setattr(fetch_reading_mod, "download_image", lambda url, destination: destination.write_bytes(b"img"))

    saved = fetch_reading_mod.process_book(books[0])
    assert saved is True
    assert (tmp_path / "reading" / "atomic-habits-james-clear.md").exists()

    other = tmp_path / "reading" / "old-book.md"
    other.write_text('book_id = "999"\nimage = "images/books/currently-reading/old.jpg"\ntitle = "Old Book"\n', encoding="utf-8")
    fetch_reading_mod.remove_books_not_in_feed(books)
    assert not other.exists()

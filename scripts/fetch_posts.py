#!/usr/bin/env python3
"""
Interactive CLI to fetch blog posts from Medium or Dev.to and convert them into Hugo content files.
"""

import argparse
import json
import pathlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Callable, Iterable, List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

import feedparser
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown
from rich.console import Console
from rich.theme import Theme

DEFAULT_MEDIUM_FEED = "https://medium.com/feed/@yrizos"
DEFAULT_DEVTO_FEED = "https://dev.to/feed/yrizos"

DEVTO_SKIP_SLUGS = {"building-a-chess-game-with-python-and-openai-3knn"}

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT_DIR / "blog"
POSTS_DIR = BLOG_DIR / "content/posts"
IMAGES_DIR = BLOG_DIR / "static/images/posts"
WEB_IMAGE_PREFIX = pathlib.Path("images/posts")

ORIGINAL_LINE_PATTERN = re.compile(r"Originally published at", re.IGNORECASE)
ORIGINAL_DATE_PATTERN = re.compile(r"on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", re.IGNORECASE)
TRACKING_IMAGE_PATTERNS = [
    re.compile(r"medium\.com/_/stat", re.IGNORECASE),
]

console = Console(theme=Theme({"prompt": "bold cyan", "choice": "bold green", "error": "bold red"}))


@dataclass
class BlogPost:
    title: str
    slug: str
    date: datetime
    original_url: str
    markdown_body: str
    tags: List[str] = field(default_factory=list)
    image_url: Optional[str] = None
    image_alt: str = ""


def slugify(title: str) -> str:
    """Convert a title into a filesystem-friendly slug."""
    normalized = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE)
    collapsed = re.sub(r"[\s_-]+", "-", normalized.strip().lower())
    return collapsed or "post"


def clean_url(url: str) -> str:
    """Remove query and fragment components from a URL."""
    split = urlsplit(url)
    return urlunsplit((split.scheme, split.netloc, split.path, "", ""))


def parse_publish_date(raw_value: Optional[str], fallback: Optional[str], title: str) -> datetime:
    """Parse publication date from the feed entry."""
    value = raw_value or fallback
    if not value:
        raise ValueError(f"Post '{title}' is missing a publish date.")
    parsed = parsedate_to_datetime(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def normalize_headings(soup: BeautifulSoup) -> None:
    """Normalize headings so the highest-level heading becomes H2, preserving hierarchy."""
    heading_nodes: List[Tuple[int, BeautifulSoup]] = []
    for level in range(1, 7):
        for heading in soup.find_all(f"h{level}"):
            heading_nodes.append((level, heading))
    if not heading_nodes:
        return
    min_level = min(level for level, _ in heading_nodes)
    offset = 2 - min_level
    for level, heading in heading_nodes:
        new_level = level + offset
        if new_level < 2:
            new_level = 2
        elif new_level > 6:
            new_level = 6
        heading.name = f"h{new_level}"


def pop_first_image(soup: BeautifulSoup) -> Tuple[Optional[str], str]:
    """Remove and return the first non-tracking image from the article body."""
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src or is_tracking_image(src):
            img.decompose()
            continue
        image_alt = img.get("alt", "")
        img.decompose()
        return src, image_alt
    return None, ""


def extract_original_metadata(soup: BeautifulSoup) -> Tuple[Optional[str], Optional[datetime]]:
    """Extract original publication URL and date from the article body."""
    for element in soup.find_all(["p", "div", "section"]):
        text = element.get_text(separator=" ", strip=True)
        if not text:
            continue
        if ORIGINAL_LINE_PATTERN.search(text):
            anchor = element.find("a", href=True)
            raw_url = anchor["href"] if anchor else None
            date_match = ORIGINAL_DATE_PATTERN.search(text)
            parsed_date: Optional[datetime] = None
            if date_match:
                date_str = date_match.group(1)
                try:
                    parsed_date = datetime.strptime(date_str, "%B %d, %Y").replace(tzinfo=timezone.utc)
                except ValueError:
                    parsed_date = None
            element.decompose()
            return clean_url(raw_url) if raw_url else None, parsed_date
    return None, None


def build_front_matter(post: BlogPost, image_web_path: Optional[pathlib.Path]) -> str:
    """Create TOML front matter for the Hugo post."""
    fields = {
        "title": post.title,
        "date": post.date.isoformat(),
        "draft": False,
        "originalURL": post.original_url,
    }
    if image_web_path:
        fields["image"] = "/" + image_web_path.as_posix()
        fields["imageAlt"] = post.image_alt or ""
    if post.tags:
        fields["tags"] = post.tags

    lines = ["+++"]
    for key, value in fields.items():
        lines.append(f"{key} = {to_toml_value(value)}")
    lines.append("+++")
    return "\n".join(lines)


def to_toml_value(value) -> str:
    """Serialize a Python value into a TOML-compatible string."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value)


def download_image(url: str, destination: pathlib.Path) -> None:
    """Download the image for the post."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as handle:
        handle.write(response.content)


def determine_image_filename(slug: str, image_url: str) -> str:
    """Determine a suitable image filename preserving the original extension when possible."""
    suffix = pathlib.Path(urlsplit(image_url).path).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        suffix = ".jpg"
    return f"{slug}{suffix}"


def write_post(post: BlogPost) -> None:
    """Write the Hugo content file and download the post image if available."""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    post_path = POSTS_DIR / f"{post.slug}.md"
    image_web_path: Optional[pathlib.Path] = None

    if post.image_url:
        image_filename = determine_image_filename(post.slug, post.image_url)
        image_path = IMAGES_DIR / image_filename
        download_image(post.image_url, image_path)
        image_web_path = WEB_IMAGE_PREFIX / image_filename

    front_matter = build_front_matter(post, image_web_path)
    post_path.write_text(f"{front_matter}\n\n{post.markdown_body}\n", encoding="utf-8")


def fetch_medium_posts(feed_url: str) -> List[BlogPost]:
    """Fetch Medium posts using the RSS feed."""
    parsed = feedparser.parse(feed_url)
    if parsed.bozo:
        raise ValueError(f"Failed to parse Medium feed: {parsed.bozo_exception}")

    posts: List[BlogPost] = []
    for entry in parsed.entries:
        title = entry.get("title")
        if not title:
            console.print("Skipping entry without a title.", style="error")
            continue

        try:
            posts.append(parse_medium_entry(entry))
        except ValueError as err:
            console.print(f"Skipping Medium entry '{title}': {err}", style="error")
    return posts


def parse_medium_entry(entry) -> BlogPost:
    """Transform a Medium feed entry into a BlogPost."""
    title: str = entry.title
    slug = slugify(title)

    published = parse_publish_date(entry.get("published"), entry.get("updated"), title)

    content_html: Optional[str] = None
    if entry.get("content"):
        content_html = entry.content[0].value
    elif entry.get("summary"):
        content_html = entry.summary
    if not content_html:
        raise ValueError("Entry does not contain HTML content.")

    soup = BeautifulSoup(content_html, "html.parser")
    override_url, override_date = extract_original_metadata(soup)
    image_url, image_alt = pop_first_image(soup)
    remove_tracking_images(soup)

    normalize_headings(soup)
    markdown_body = html_to_markdown(str(soup), heading_style="ATX").strip()

    original_url = override_url or entry.get("link")
    if not original_url:
        raise ValueError("Entry is missing the original URL.")
    original_url = clean_url(original_url)

    if override_date:
        published = override_date

    return BlogPost(
        title=title,
        slug=slug,
        date=published,
        original_url=original_url,
        markdown_body=markdown_body,
        tags=extract_tags(entry),
        image_url=image_url,
        image_alt=image_alt,
    )


def fetch_devto_posts(feed_url: str) -> List[BlogPost]:
    """Fetch Dev.to posts using the RSS feed."""
    parsed = feedparser.parse(feed_url)
    if parsed.bozo:
        raise ValueError(f"Failed to parse Dev.to feed: {parsed.bozo_exception}")

    posts: List[BlogPost] = []
    for entry in parsed.entries:
        title = entry.get("title")
        if not title:
            console.print("Skipping entry without a title.", style="error")
            continue
        entry_slug = extract_devto_slug(entry)
        if entry_slug and entry_slug in DEVTO_SKIP_SLUGS:
            continue
        try:
            posts.append(parse_devto_entry(entry))
        except ValueError as err:
            console.print(f"Skipping Dev.to entry '{title}': {err}", style="error")
    return posts


def parse_devto_entry(entry) -> BlogPost:
    """Transform a Dev.to feed entry into a BlogPost."""
    title: str = entry.title
    slug = slugify(title)

    published = parse_publish_date(entry.get("published"), entry.get("updated"), title)

    content_html: Optional[str] = None
    if entry.get("content"):
        content_html = entry.content[0].value
    elif entry.get("summary"):
        content_html = entry.summary
    if not content_html:
        raise ValueError("Entry does not contain HTML content.")

    soup = BeautifulSoup(content_html, "html.parser")
    image_url, image_alt = pop_first_image(soup)
    if not image_url:
        thumbnails = entry.get("media_thumbnail")
        if thumbnails and isinstance(thumbnails, list):
            thumb = thumbnails[0]
            if isinstance(thumb, dict) and thumb.get("url"):
                image_url = thumb["url"]
                image_alt = thumb.get("title", "")

    remove_tracking_images(soup)
    normalize_headings(soup)
    markdown_body = html_to_markdown(str(soup), heading_style="ATX").strip()

    original_url = entry.get("link") or entry.get("url")
    if not original_url:
        raise ValueError("Entry is missing the original URL.")
    original_url = clean_url(original_url)

    return BlogPost(
        title=title,
        slug=slug,
        date=published,
        original_url=original_url,
        markdown_body=markdown_body,
        tags=extract_tags(entry),
        image_url=image_url,
        image_alt=image_alt,
    )


def extract_devto_slug(entry) -> Optional[str]:
    """Extract the slug portion from a Dev.to entry link."""
    link = entry.get("link")
    if not link:
        return None
    path = urlsplit(link).path
    if not path:
        return None
    parts = [part for part in path.split("/") if part]
    if len(parts) < 2:
        return None
    return parts[-1]


def extract_tags(entry) -> List[str]:
    """Extract tag terms from a feed entry."""
    tags: List[str] = []
    seen = set()
    for tag in entry.get("tags", []):
        term = tag.get("term") if isinstance(tag, dict) else getattr(tag, "term", None)
        if not term:
            continue
        normalized = str(term).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        tags.append(normalized)
    return tags


def is_tracking_image(url: str) -> bool:
    """Return True if the URL looks like a known tracking pixel."""
    normalized = url.lower()
    for pattern in TRACKING_IMAGE_PATTERNS:
        if pattern.search(normalized):
            return True
    return False


def remove_tracking_images(soup: BeautifulSoup) -> None:
    """Strip any remaining tracking images from the article body."""
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src or is_tracking_image(src):
            img.decompose()


def prompt_source() -> str:
    """Prompt the user to pick a source feed."""
    console.print("\nWhere should I fetch posts from today?", style="choice")
    console.print("[1] Medium")
    console.print("[2] Dev.to")
    console.print("[3] Exit")

    while True:
        selection = console.input("[prompt]Enter your choice (1/2/3): [/prompt]").strip()
        if selection == "1":
            return "medium"
        if selection == "2":
            return "devto"
        if selection == "3":
            return "exit"
        console.print("Please choose 1, 2, or 3.", style="error")


def prompt_for_post(post: BlogPost) -> str:
    """Prompt the user whether to fetch a specific post."""
    console.print(
        f"\n[choice]{post.title}[/choice]\n  Published: {post.date.strftime('%Y-%m-%d')}\n  URL: {post.original_url}"
    )
    while True:
        decision = console.input("[prompt]Fetch this post? (yes/no/exit): [/prompt]").strip().lower()
        if decision in {"yes", "y"}:
            return "yes"
        if decision in {"no", "n"}:
            return "no"
        if decision in {"exit", "e"}:
            return "exit"
        console.print("Please answer with 'yes', 'no', or 'exit'.", style="error")


def process_posts(posts: Iterable[BlogPost]) -> None:
    """Iterate through posts, prompting the user before writing each one."""
    for post in posts:
        decision = prompt_for_post(post)
        if decision == "exit":
            console.print("Alright, stopping here. Catch you next time! 👋", style="choice")
            break
        if decision == "no":
            console.print(f"Skipping: {post.title}", style="choice")
            continue
        try:
            write_post(post)
            console.print(f"Saved: {post.title}", style="choice")
        except Exception as err:  # noqa: BLE001
            console.print(f"Failed to save '{post.title}': {err}", style="error")


def run(feed_fetcher: Callable[[str], List[BlogPost]], feed_url: str) -> None:
    """Fetch posts from the selected feed and process them."""
    posts = feed_fetcher(feed_url)
    if not posts:
        console.print("No posts found to process.", style="error")
        return
    console.print(f"\nFetched {len(posts)} posts. Let's pick which ones to keep!", style="choice")
    process_posts(posts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch posts from Medium or Dev.to and convert to Hugo content.")
    parser.add_argument("--medium-feed", default=DEFAULT_MEDIUM_FEED, help="Medium RSS feed URL.")
    parser.add_argument("--devto-feed", default=DEFAULT_DEVTO_FEED, help="Dev.to RSS feed URL.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = prompt_source()
    if source == "exit":
        console.print("Nothing fetched this time. See you soon! ✨", style="choice")
        return
    if source == "medium":
        run(fetch_medium_posts, args.medium_feed)
    elif source == "devto":
        run(fetch_devto_posts, args.devto_feed)


if __name__ == "__main__":
    main()

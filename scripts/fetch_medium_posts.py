#!/usr/bin/env python3
"""
Fetch posts from the Medium feed and convert them into Hugo content files.
"""

import argparse
import json
import pathlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

import feedparser
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

DEFAULT_FEED_URL = "https://medium.com/feed/@yrizos"
ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT_DIR / "blog"
POSTS_DIR = BLOG_DIR / "content/posts"
IMAGES_DIR = BLOG_DIR / "static/images/posts"
WEB_IMAGE_PREFIX = pathlib.Path("images/posts")
ORIGINAL_LINE_PATTERN = re.compile(r"Originally published at", re.IGNORECASE)
ORIGINAL_DATE_PATTERN = re.compile(
    r"on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", re.IGNORECASE
)


@dataclass
class MediumPost:
    title: str
    slug: str
    date: datetime
    image_url: str
    image_alt: str
    original_url: str
    markdown_body: str


def slugify(title: str) -> str:
    """Convert a title into a filesystem-friendly slug."""
    normalized = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE)
    collapsed = re.sub(r"[\s_-]+", "-", normalized.strip().lower())
    return collapsed or "post"


def clean_url(url: str) -> str:
    """Remove query and fragment components from a URL."""
    split = urlsplit(url)
    return urlunsplit((split.scheme, split.netloc, split.path, "", ""))


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


def parse_entry(entry) -> MediumPost:
    """Transform a raw feed entry into a MediumPost."""
    if not entry.get("title"):
        raise ValueError("Feed entry is missing a title.")

    title: str = entry.title
    slug = slugify(title)

    published: Optional[datetime] = None
    published_str = entry.get("published")
    if published_str:
        published = parsedate_to_datetime(published_str)
    elif entry.get("updated"):
        published = parsedate_to_datetime(entry.updated)
    if not published:
        raise ValueError(f"Post '{title}' is missing a publish date.")
    if published.tzinfo is None:
        published = published.replace(tzinfo=timezone.utc)

    content_html: Optional[str] = None
    if entry.get("content"):
        content_html = entry.content[0].value
    elif entry.get("summary"):
        content_html = entry.summary
    if not content_html:
        raise ValueError(f"Post '{title}' does not contain HTML content.")

    soup = BeautifulSoup(content_html, "html.parser")
    override_url, override_date = extract_original_metadata(soup)
    img = soup.find("img")
    if not img or not img.get("src"):
        raise ValueError(f"Post '{title}' does not contain an image.")

    image_url = img["src"]
    image_alt = img.get("alt", "")
    img.decompose()

    # Normalize headings so the highest-level heading becomes H2, preserving hierarchy.
    heading_nodes = []
    for level in range(1, 7):
        for heading in soup.find_all(f"h{level}"):
            heading_nodes.append((level, heading))

    if heading_nodes:
        min_level = min(level for level, _ in heading_nodes)
        offset = 2 - min_level
        for level, heading in heading_nodes:
            new_level = level + offset
            if new_level < 2:
                new_level = 2
            elif new_level > 6:
                new_level = 6
            heading.name = f"h{new_level}"

    markdown_body = html_to_markdown(str(soup), heading_style="ATX")

    original_url = override_url or entry.get("link")
    if not original_url:
        raise ValueError(f"Post '{title}' is missing the original URL.")
    original_url = clean_url(original_url)

    if override_date:
        published = override_date

    return MediumPost(
        title=title,
        slug=slug,
        date=published,
        image_url=image_url,
        image_alt=image_alt,
        original_url=original_url,
        markdown_body=markdown_body.strip(),
    )


def to_toml_value(value) -> str:
    """Serialize a Python value into a TOML-compatible string."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value)


def prompt_user(title: str) -> str:
    """Prompt the user to decide whether a post should be fetched."""
    prompt = f"Should I fetch: {title}? (yes/no/exit): "
    while True:
        choice = input(prompt).strip().lower()
        if choice in {"yes", "y"}:
            return "yes"
        if choice in {"no", "n"}:
            return "no"
        if choice in {"exit", "e"}:
            return "exit"
        print("Please answer with 'yes', 'no', or 'exit'.")


def build_front_matter(post: MediumPost, image_web_path: pathlib.Path) -> str:
    """Create TOML front matter for the Hugo post."""
    fields = {
        "title": post.title,
        "date": post.date.isoformat(),
        "draft": False,
        "image": "/" + image_web_path.as_posix(),
        "imageAlt": post.image_alt,
        "originalURL": post.original_url,
    }

    lines = ["+++"]
    for key, value in fields.items():
        lines.append(f"{key} = {to_toml_value(value)}")
    lines.append("+++")
    return "\n".join(lines)


def download_image(url: str, destination: pathlib.Path) -> None:
    """Download the image for the post."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as handle:
        handle.write(response.content)


def write_post(post: MediumPost) -> None:
    """Write the Hugo content file and download the post image."""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    post_path = POSTS_DIR / f"{post.slug}.md"
    image_path = IMAGES_DIR / f"{post.slug}.jpg"
    image_web_path = WEB_IMAGE_PREFIX / f"{post.slug}.jpg"

    download_image(post.image_url, image_path)

    front_matter = build_front_matter(post, image_web_path)
    post_path.write_text(f"{front_matter}\n\n{post.markdown_body}\n", encoding="utf-8")


def fetch_posts(feed_url: str) -> None:
    """Fetch the feed and process entries interactively."""
    parsed = feedparser.parse(feed_url)
    if parsed.bozo:
        raise ValueError(f"Failed to parse feed: {parsed.bozo_exception}")

    for entry in parsed.entries:
        title = entry.get("title") or "(untitled post)"
        decision = prompt_user(title)
        if decision == "exit":
            print("Exiting without processing remaining posts.")
            break
        if decision == "no":
            print(f"Skipping: {title}")
            continue
        try:
            post = parse_entry(entry)
            write_post(post)
            print(f"Processed post: {post.title}")
        except ValueError as err:
            print(f"Skipping entry: {err}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Medium posts and convert to Hugo content.")
    parser.add_argument("--feed", default=DEFAULT_FEED_URL, help="Medium feed URL to fetch.")
    args = parser.parse_args()

    fetch_posts(args.feed)


if __name__ == "__main__":
    main()

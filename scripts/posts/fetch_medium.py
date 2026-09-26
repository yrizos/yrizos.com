"""Medium-specific post fetching logic."""

import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit

import feedparser
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown
from rich.console import Console
from rich.theme import Theme

from .blog_post import BlogPost
from .cli import clean_url, parse_publish_date, slugify

console = Console(
    theme=Theme({"prompt": "bold cyan", "choice": "bold green", "error": "bold red"})
)

ORIGINAL_LINE_PATTERN = re.compile(r"Originally published at", re.IGNORECASE)
ORIGINAL_DATE_PATTERN = re.compile(
    r"on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", re.IGNORECASE
)
TRACKING_IMAGE_PATTERNS = [
    re.compile(r"medium\.com/_/stat", re.IGNORECASE),
]


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


def extract_original_metadata(
    soup: BeautifulSoup,
) -> Tuple[Optional[str], Optional[datetime]]:
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
                    parsed_date = datetime.strptime(date_str, "%B %d, %Y").replace(
                        tzinfo=timezone.utc
                    )
                except ValueError:
                    parsed_date = None
            element.decompose()
            return clean_url(raw_url) if raw_url else None, parsed_date
    return None, None


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

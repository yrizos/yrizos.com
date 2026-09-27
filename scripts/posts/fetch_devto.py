"""Dev.to-specific post fetching logic."""

import html
import re
from urllib.parse import urlsplit

import feedparser
import requests
from rich.console import Console
from rich.theme import Theme

from .blog_post import BlogPost
from .cli import clean_url, extract_tags, parse_publish_date, slugify

console = Console(
    theme=Theme({"prompt": "bold cyan", "choice": "bold green", "error": "bold red"})
)

DEVTO_SKIP_SLUGS = {"building-a-chess-game-with-python-and-openai-3knn"}


def extract_devto_article_id(url: str) -> str | None:
    """Extract the article path (username/slug) from a Dev.to URL."""
    path = urlsplit(url).path
    if not path:
        return None
    path = path.lstrip("/")
    parts = [part for part in path.split("/") if part]
    if len(parts) < 2:
        return None
    # Dev.to URLs are formatted like: /username/title-slug-id
    # The API expects: username/title-slug-id
    return f"{parts[0]}/{parts[1]}"


def fetch_devto_article(article_id: str) -> dict:
    """Fetch article data from the Dev.to API."""
    api_url = f"https://dev.to/api/articles/{article_id}"
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_series_title(username: str, collection_id: int) -> str | None:
    """Fetch series title from the Dev.to series page."""
    series_url = f"https://dev.to/{username}/series/{collection_id}"
    try:
        response = requests.get(series_url, timeout=30)
        response.raise_for_status()
    except requests.RequestException:
        return None

    match = re.search(r"<title>(.+?)</title>", response.text)
    if not match:
        return None
    title = html.unescape(match.group(1))
    title = re.sub(r"\s+Series['\u2019]?\s+Articles\s*-\s*DEV Community.*$", "", title)
    return title.strip()


def calculate_series_order(
    username: str, collection_id: int, article_id: int
) -> int | None:
    """Calculate the article's position in the series based on publish date."""
    api_url = f"https://dev.to/api/articles?username={username}&per_page=1000"
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        articles = response.json()
    except (requests.RequestException, ValueError):
        return None

    series_articles = [a for a in articles if a.get("collection_id") == collection_id]
    series_articles.sort(key=lambda x: x.get("published_at", ""))
    for index, article in enumerate(series_articles, start=1):
        if article.get("id") == article_id:
            return index
    return None


def extract_devto_slug(entry) -> str | None:
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


def fetch_devto_posts(feed_url: str) -> list[BlogPost]:
    """Fetch Dev.to posts using the RSS feed."""
    parsed = feedparser.parse(feed_url)
    if parsed.bozo:
        raise ValueError(f"Failed to parse Dev.to feed: {parsed.bozo_exception}")

    posts: list[BlogPost] = []
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
    """Transform a Dev.to feed entry into a BlogPost using the Dev.to API."""
    title: str = entry.title
    slug = slugify(title)

    published = parse_publish_date(entry.get("published"), entry.get("updated"), title)

    original_url = entry.get("link") or entry.get("url")
    if not original_url:
        raise ValueError("Entry is missing the original URL.")
    original_url = clean_url(original_url)

    article_id = extract_devto_article_id(original_url)
    if not article_id:
        raise ValueError("Could not extract article ID from Dev.to URL.")

    api_data = fetch_devto_article(article_id)
    markdown_body = api_data.get("body_markdown", "").strip()
    if not markdown_body:
        raise ValueError("Article does not contain markdown content.")

    image_url = api_data.get("cover_image")
    image_alt = api_data.get("title", "")

    # Fallback to feed thumbnail if no cover image
    if not image_url:
        thumbnails = entry.get("media_thumbnail")
        if thumbnails and isinstance(thumbnails, list):
            thumb = thumbnails[0]
            if isinstance(thumb, dict) and thumb.get("url"):
                image_url = thumb["url"]
                image_alt = thumb.get("title", "")

    tag_list = api_data.get("tag_list", [])
    # Handle both list and comma-separated string formats from API
    if isinstance(tag_list, str):
        tags = [tag.strip() for tag in tag_list.split(",") if tag.strip()]
    elif isinstance(tag_list, list):
        tags = [str(tag).strip() for tag in tag_list if tag]
    else:
        tags = []

    # Extract series information if article is part of a series
    series_title = None
    series_order = None
    collection_id = api_data.get("collection_id")
    if collection_id:
        # Extract username from article_id (format: "username/slug")
        username = article_id.split("/")[0] if "/" in article_id else None
        if username:
            series_title = fetch_series_title(username, collection_id)
            article_numeric_id = api_data.get("id")
            if article_numeric_id:
                series_order = calculate_series_order(
                    username, collection_id, article_numeric_id
                )

    return BlogPost(
        title=title,
        slug=slug,
        date=published,
        original_url=original_url,
        markdown_body=markdown_body,
        tags=tags if tags else extract_tags(entry),
        image_url=image_url,
        image_alt=image_alt,
        series_title=series_title,
        series_order=series_order,
    )

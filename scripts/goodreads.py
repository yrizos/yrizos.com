"""Shared Goodreads book-fetching helpers used by fetch_books.py and fetch_reading.py."""

import pathlib
import re
from collections.abc import Callable
from datetime import datetime
from typing import Optional, Tuple
from urllib.parse import urlparse

import requests

USER_AGENT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}
BOOK_ID_RE = re.compile(r'book_id\s*=\s*"([^"]+)"')
IMAGE_PATH_RE = re.compile(r'image\s*=\s*"([^"]+)"')


def slugify(text: str) -> str:
    """Convert text to a filesystem-friendly slug."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")


def clean_goodreads_url(url: str) -> str:
    """Strip Goodreads' RSS tracking query params from a URL."""
    return url.replace("?utm_medium=api&utm_source=rss", "").replace(
        "&utm_medium=api&utm_source=rss", ""
    )


def parse_goodreads_date(raw: str) -> Optional[str]:
    """Parse a Goodreads RSS date into YYYY-MM-DD, or None if unparseable."""
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return None


def _google_books_image(query: str) -> Optional[str]:
    """Query the Google Books API and return the best cover image URL, if any."""
    try:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={query}", timeout=5
        )
        if response.status_code != 200:
            return None
        items = response.json().get("items") or []
    except (requests.RequestException, ValueError):
        return None
    if not items:
        return None
    image_links = items[0].get("volumeInfo", {}).get("imageLinks", {})
    return image_links.get("extraLarge") or image_links.get("large")


def _isbn_cover_url(isbn_clean: str) -> Optional[str]:
    """Return the Open Library cover URL for an ISBN if it actually resolves."""
    url = f"https://covers.openlibrary.org/b/isbn/{isbn_clean}-L.jpg"
    try:
        response = requests.head(url, timeout=5)
    except requests.RequestException:
        return None
    return url if response.status_code == 200 else None


def _openlibrary_search_cover(query: str) -> Optional[str]:
    """Search Open Library by title/author and return a cover URL, if any."""
    try:
        response = requests.get(
            f"https://openlibrary.org/search.json?q={query}&limit=1", timeout=5
        )
        if response.status_code != 200:
            return None
        docs = response.json().get("docs") or []
    except (requests.RequestException, ValueError):
        return None
    cover_id = docs[0].get("cover_i") if docs else None
    return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else None


def get_image_url_from_sources(
    book_id: str, isbn: str, title: str, author: str
) -> Optional[str]:
    """Try Open Library and Google Books to find a book cover image URL."""
    isbn_clean = isbn.strip() if isbn else ""
    if len(isbn_clean) >= 10:
        image_url = _isbn_cover_url(isbn_clean) or _google_books_image(
            f"isbn:{isbn_clean}"
        )
        if image_url:
            return image_url

    if title:
        query = f"{title}{' ' + author if author else ''}".replace(" ", "+")
        image_url = _google_books_image(query) or _openlibrary_search_cover(query)
        if image_url:
            return image_url

    return None


def download_image(url: str, destination: pathlib.Path) -> None:
    """Download an image from a URL to a local destination."""
    session = requests.Session()
    session.headers.update(USER_AGENT_HEADERS)
    if "goodreads.com" in url or "gr-assets.com" in url:
        session.headers["Referer"] = "https://www.goodreads.com/"

    response = session.get(url, timeout=30)
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)


def determine_image_filename(slug: str, image_url: str) -> str:
    """Determine an image filename preserving the original extension when recognized."""
    suffix = pathlib.Path(urlparse(image_url).path).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        suffix = ".jpg"
    return f"{slug}{suffix}"


def _escape_toml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def to_toml_value(value) -> str:
    """Convert a Python value to TOML format."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return f"[{', '.join(_escape_toml_string(item) for item in value)}]"
    return _escape_toml_string(str(value))


def read_book_id_and_image(content: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract the book_id and image path from a content file's front matter."""
    book_id_match = BOOK_ID_RE.search(content)
    image_match = IMAGE_PATH_RE.search(content)
    return (
        book_id_match.group(1) if book_id_match else None,
        image_match.group(1) if image_match else None,
    )


def delete_book(
    book_file: pathlib.Path, images_dir: pathlib.Path, image_path: Optional[str]
) -> None:
    """Delete a book content file and its cover image, if any."""
    book_file.unlink()
    if image_path:
        image_file = images_dir / pathlib.Path(image_path).name
        if image_file.exists():
            image_file.unlink()


def remove_books_where(
    books_dir: pathlib.Path,
    images_dir: pathlib.Path,
    should_remove: Callable[[str], bool],
) -> int:
    """Delete book files (and their cover images) whose book_id matches should_remove."""
    if not books_dir.exists():
        return 0
    removed = 0
    for book_file in books_dir.glob("*.md"):
        book_id, image_path = read_book_id_and_image(
            book_file.read_text(encoding="utf-8")
        )
        if book_id and should_remove(book_id):
            delete_book(book_file, images_dir, image_path)
            removed += 1
            print(f"Removed: {book_file.stem}")
    return removed

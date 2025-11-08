#!/usr/bin/env python3
"""Fetch 4 and 5 star read books from Goodreads RSS feed."""

import feedparser
import requests
import pathlib
import re
from typing import List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
from datetime import datetime

GOODREADS_FEED = "https://www.goodreads.com/review/list_rss/68793210?key=Q5sTrEOdYsUhUSrXK0J7wg9adkkcAuTFlIKN8-TetPnEWK2-&shelf=read"

SKIP_BOOK_IDS = {"29630264", "40186304", "32855235", "7930361160", "216017751", "41832736", "16146899", "46184813", "64238935", "5973243", "6416196", "17340660", "60233239", "36223859", "57987464", "8176978", "36844711", "56377548", "8442726", "6567483", "56791389", "126917757", "6488124", "52949193", "18938240", "20572455", "8123311", "6219313", "62193738"}

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT_DIR / "blog"
BOOKS_DIR = BLOG_DIR / "content/books/read"
IMAGES_DIR = BLOG_DIR / "assets/images/books/read"


@dataclass
class Book:
    title: str
    author: str
    slug: str
    goodreads_url: str
    book_id: str
    isbn: str
    rating: str
    date_read: str
    image_url: Optional[str] = None


def slugify(text: str) -> str:
    """Convert text to a filesystem-friendly slug."""
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    return slug


def get_image_url_from_sources(book_id: str, isbn: str, title: str, author: str) -> Optional[str]:
    """Try multiple sources to get book cover image URL."""
    # Try Open Library by ISBN
    if isbn:
        isbn_clean = isbn.strip()
        if isbn_clean and len(isbn_clean) >= 10:
            url = f"https://covers.openlibrary.org/b/isbn/{isbn_clean}-L.jpg"
            # Test if URL exists
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    return url
            except Exception:
                pass

    # Try Google Books API by ISBN
    if isbn:
        isbn_clean = isbn.strip()
        if isbn_clean and len(isbn_clean) >= 10:
            try:
                google_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_clean}"
                response = requests.get(google_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("items") and len(data["items"]) > 0:
                        image_links = data["items"][0].get(
                            "volumeInfo", {}).get("imageLinks", {})
                        if image_links.get("extraLarge"):
                            return image_links.get("extraLarge")
                        if image_links.get("large"):
                            return image_links.get("large")
            except Exception:
                pass

    # Try Google Books API by title + author
    if title and author:
        try:
            query = f"{title} {author}".replace(" ", "+")
            google_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
            response = requests.get(google_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("items") and len(data["items"]) > 0:
                    image_links = data["items"][0].get(
                        "volumeInfo", {}).get("imageLinks", {})
                    if image_links.get("extraLarge"):
                        return image_links.get("extraLarge")
                    if image_links.get("large"):
                        return image_links.get("large")
        except Exception:
            pass

    # Try Open Library Search API
    if title:
        try:
            query = f"{title}".replace(" ", "+")
            if author:
                query += f"+{author}".replace(" ", "+")
            open_lib_url = f"https://openlibrary.org/search.json?q={query}&limit=1"
            response = requests.get(open_lib_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("docs") and len(data["docs"]) > 0:
                    cover_id = data["docs"][0].get("cover_i")
                    if cover_id:
                        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        except Exception:
            pass

    return None


def to_toml_value(value) -> str:
    """Convert a Python value to TOML format."""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        # Escape quotes and backslashes
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    return f'"{str(value)}"'


def build_front_matter(book: Book, image_path: str) -> str:
    """Build TOML front matter."""
    fields = {
        "title": book.title,
        "author": book.author,
        "draft": False,
        "goodreads_url": book.goodreads_url,
        "book_id": book.book_id,
        "isbn": book.isbn,
        "rating": book.rating,
        "date_read": book.date_read,
        "image": image_path,
    }

    lines = ["+++"]
    for key, value in fields.items():
        lines.append(f"{key} = {to_toml_value(value)}")
    lines.append("+++")
    return "\n".join(lines)


def fetch_goodreads_books() -> List[Book]:
    """Fetch books from Goodreads RSS feed."""
    feed = feedparser.parse(GOODREADS_FEED)

    if feed.bozo:
        print(f"Error parsing RSS feed: {feed.bozo_exception}")
        return []

    books = []
    for entry in feed.entries:
        book_id = entry.get("book_id", "").strip()
        if book_id in SKIP_BOOK_IDS:
            continue

        # Filter for 4 and 5 star ratings
        rating = entry.get("user_rating", "").strip()
        if rating not in ["4", "5"]:
            continue

        title = entry.get("title", "").strip()
        author = entry.get("author_name", "").strip()
        isbn = entry.get("isbn", "").strip()
        goodreads_url = entry.get("link", "").strip()

        # Remove utm_medium and utm_source query parameters
        if goodreads_url:
            if "?utm_medium=api&utm_source=rss" in goodreads_url:
                goodreads_url = goodreads_url.replace(
                    "?utm_medium=api&utm_source=rss", "")
            elif "&utm_medium=api&utm_source=rss" in goodreads_url:
                goodreads_url = goodreads_url.replace(
                    "&utm_medium=api&utm_source=rss", "")

        # Get date read and convert to ISO format (YYYY-MM-DD) for Hugo
        date_read_raw = entry.get("user_read_at", "").strip() or entry.get("user_date_added", "").strip()
        date_read = ""
        if date_read_raw:
            try:
                # Parse RFC 822 format date
                dt = datetime.strptime(date_read_raw, "%a, %d %b %Y %H:%M:%S %z")
                # Convert to ISO format (YYYY-MM-DD)
                date_read = dt.strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                # If parsing fails, keep original
                date_read = date_read_raw

        # Get image URL from RSS
        image_url = entry.get("book_large_image_url",
                              "") or entry.get("book_image_url", "")
        image_url = image_url.strip() if image_url else None

        slug = slugify(f"{title}-{author}")

        books.append(Book(
            title=title,
            author=author,
            slug=slug,
            goodreads_url=goodreads_url,
            book_id=book_id,
            isbn=isbn,
            rating=rating,
            date_read=date_read,
            image_url=image_url,
        ))

    return books


def download_image(url: str, destination: pathlib.Path) -> None:
    """Download image from URL."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    })

    if "goodreads.com" in url or "gr-assets.com" in url:
        session.headers["Referer"] = "https://www.goodreads.com/"

    response = session.get(url, timeout=30)
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as handle:
        handle.write(response.content)


def determine_image_filename(slug: str, image_url: str) -> str:
    """Determine image filename preserving extension."""
    suffix = pathlib.Path(urlparse(image_url).path).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        suffix = ".jpg"
    return f"{slug}{suffix}"


def process_book(book: Book) -> bool:
    """Process a single book: download image and create content file."""
    book_file = BOOKS_DIR / f"{book.slug}.md"
    
    # Skip if already exists
    if book_file.exists():
        return False

    # Try to get image URL
    image_url = book.image_url

    # If no image from RSS, try alternative sources
    if not image_url:
        image_url = get_image_url_from_sources(
            book.book_id, book.isbn, book.title, book.author)

    if not image_url:
        print(f"Skipping '{book.title}' - no image available")
        return False

    # Determine image filename and path
    image_filename = determine_image_filename(book.slug, image_url)
    image_path_local = IMAGES_DIR / image_filename

    # Download image (skip if already exists)
    if not image_path_local.exists():
        try:
            download_image(image_url, image_path_local)
        except Exception as err:
            print(f"Failed to download image for '{book.title}': {err}")
            return False

    # Create content file
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)

    # Image path relative to assets/
    image_path_relative = f"images/books/read/{image_filename}"

    front_matter = build_front_matter(book, image_path_relative)
    content = f"{front_matter}\n\n"

    book_file.write_text(content, encoding="utf-8")
    print(f"Saved: {book.title}")
    return True


def remove_skipped_books() -> None:
    """Remove existing books that are in the skip list."""
    if not BOOKS_DIR.exists():
        return

    removed_count = 0
    for book_file in BOOKS_DIR.glob("*.md"):
        try:
            content = book_file.read_text(encoding="utf-8")
            book_id_match = re.search(r'book_id\s*=\s*"([^"]+)"', content)
            if book_id_match:
                book_id = book_id_match.group(1)
                if book_id in SKIP_BOOK_IDS:
                    # Delete the book file
                    book_file.unlink()
                    # Delete the image if it exists
                    image_match = re.search(r'image\s*=\s*"([^"]+)"', content)
                    if image_match:
                        image_path = image_match.group(1)
                        image_file = IMAGES_DIR / pathlib.Path(image_path).name
                        if image_file.exists():
                            image_file.unlink()
                    removed_count += 1
                    print(f"Removed skipped book: {book_file.stem}")
        except Exception as err:
            print(f"Error checking {book_file.name}: {err}")
            continue

    if removed_count > 0:
        print(f"Removed {removed_count} books from skip list.")


def main() -> None:
    """Main entry point."""
    print("Fetching 4 and 5 star read books from Goodreads...")

    # Remove existing books that are in skip list
    remove_skipped_books()

    books = fetch_goodreads_books()

    if not books:
        print("No books found matching criteria.")
        return

    print(f"Found {len(books)} books matching criteria.")

    saved_count = 0
    skipped_count = 0

    for book in books:
        if process_book(book):
            saved_count += 1
        else:
            skipped_count += 1

    print(f"\nSaved: {saved_count}, Skipped: {skipped_count}")


if __name__ == "__main__":
    main()


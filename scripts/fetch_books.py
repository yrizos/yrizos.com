#!/usr/bin/env python3
"""Fetch favorite books from Goodreads RSS feed."""

import pathlib
import sys
from dataclasses import dataclass, field

import feedparser
import requests

scripts_dir = pathlib.Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

import goodreads
from goodreads import (
    determine_image_filename,
    download_image,
    get_image_url_from_sources,
    slugify,
    to_toml_value,
)

GOODREADS_FEED = "https://www.goodreads.com/review/list_rss/68793210?key=Q5sTrEOdYsUhUSrXK0J7wg9adkkcAuTFlIKN8-TetPnEWK2-&shelf=favorites"

SKIP_BOOK_IDS = {
    "29630264",
    "40186304",
    "32855235",
    "7930361160",
    "216017751",
    "41832736",
    "16146899",
    "46184813",
    "64238935",
    "5973243",
    "6416196",
    "17340660",
    "60233239",
    "36223859",
    "57987464",
    "8176978",
    "36844711",
    "56377548",
    "8442726",
    "6567483",
    "56791389",
    "126917757",
    "6488124",
    "52949193",
    "18938240",
    "20572455",
    "8123311",
    "6219313",
    "62193738",
    "40053399",
    "43812338",
    "34810395",
    "40396699",
}

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT_DIR / "blog"
BOOKS_DIR = BLOG_DIR / "content/books/recommendations"
IMAGES_DIR = BLOG_DIR / "assets/images/books/recommendations"


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
    image_url: str | None = None
    tags: list[str] = field(default_factory=list)


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
        "image": image_path,
    }

    if book.date_read:
        fields["date_read"] = book.date_read
    if book.tags:
        fields["tags"] = book.tags

    lines = ["+++"]
    for key, value in fields.items():
        lines.append(f"{key} = {to_toml_value(value)}")
    lines.append("+++")
    return "\n".join(lines)


def fetch_goodreads_books() -> list[Book]:
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

        title = entry.get("title", "").strip()
        author = entry.get("author_name", "").strip()
        isbn = entry.get("isbn", "").strip()
        goodreads_url = goodreads.clean_goodreads_url(entry.get("link", "").strip())
        rating = entry.get("user_rating", "").strip()

        # Only use user_read_at, not user_date_added (which is when added to favorites)
        date_read_raw = entry.get("user_read_at", "").strip()
        date_read = goodreads.parse_goodreads_date(date_read_raw) or date_read_raw

        image_url = entry.get("book_large_image_url", "") or entry.get(
            "book_image_url", ""
        )
        image_url = image_url.strip() if image_url else None

        user_shelves = entry.get("user_shelves", "")
        tags = [
            tag.strip()
            for tag in str(user_shelves).split(",")
            if tag.strip() and tag.strip().lower() != "favorites"
        ]

        slug = slugify(f"{title}-{author}")

        books.append(
            Book(
                title=title,
                author=author,
                slug=slug,
                goodreads_url=goodreads_url,
                book_id=book_id,
                isbn=isbn,
                rating=rating,
                date_read=date_read,
                image_url=image_url,
                tags=tags,
            )
        )

    return books


def _find_existing_book(book_id: str) -> tuple[pathlib.Path | None, str | None]:
    """Find an existing book file by book_id, returning (file, image_path)."""
    if not BOOKS_DIR.exists():
        return None, None
    for book_file in BOOKS_DIR.glob("*.md"):
        existing_book_id, image_path = goodreads.read_book_id_and_image(
            book_file.read_text(encoding="utf-8")
        )
        if existing_book_id == book_id:
            return book_file, image_path
    return None, None


def _ensure_image(book: Book) -> str | None:
    """Download the book's cover image if needed, returning its path relative to assets/."""
    image_url = book.image_url or get_image_url_from_sources(
        book.book_id, book.isbn, book.title, book.author
    )
    if not image_url:
        return None

    image_filename = determine_image_filename(book.slug, image_url)
    image_path_local = IMAGES_DIR / image_filename
    if not image_path_local.exists():
        try:
            download_image(image_url, image_path_local)
        except (requests.RequestException, OSError) as err:
            print(f"Failed to download image for '{book.title}': {err}")
            return None

    return f"images/books/recommendations/{image_filename}"


def process_book(book: Book) -> tuple[bool, str]:
    """Process a single book: download image and create content file, or update existing.

    Returns:
        tuple[bool, str]: (success, action) where action is "created", "updated", or "skipped"
    """
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)

    existing_file, existing_image_path = _find_existing_book(book.book_id)

    if existing_file:
        image_path_relative = existing_image_path or _ensure_image(book)
        if not image_path_relative:
            print(f"Skipping update for '{book.title}' - no image available")
            return False, "skipped"

        front_matter = build_front_matter(book, image_path_relative)
        existing_file.write_text(f"{front_matter}\n\n", encoding="utf-8")
        print(f"Updated: {book.title}")
        return True, "updated"

    image_path_relative = _ensure_image(book)
    if not image_path_relative:
        print(f"Skipping '{book.title}' - no image available")
        return False, "skipped"

    book_file = BOOKS_DIR / f"{book.slug}.md"
    front_matter = build_front_matter(book, image_path_relative)
    book_file.write_text(f"{front_matter}\n\n", encoding="utf-8")
    print(f"Created: {book.title}")
    return True, "created"


def remove_skipped_books() -> None:
    """Remove existing books that are in the skip list."""
    removed = goodreads.remove_books_where(
        BOOKS_DIR, IMAGES_DIR, lambda book_id: book_id in SKIP_BOOK_IDS
    )
    if removed:
        print(f"Removed {removed} books from skip list.")


def remove_books_not_in_feed(feed_book_ids: set) -> None:
    """Remove existing books that are not in the feed (and not in the skip list)."""
    removed = goodreads.remove_books_where(
        BOOKS_DIR,
        IMAGES_DIR,
        lambda book_id: book_id not in SKIP_BOOK_IDS and book_id not in feed_book_ids,
    )
    if removed:
        print(f"Removed {removed} books not in feed.")


def remove_duplicate_books() -> None:
    """Remove duplicate books that have the same book_id, keeping the longest content."""
    if not BOOKS_DIR.exists():
        return

    books_by_id: dict[str, list[tuple[pathlib.Path, str]]] = {}
    for book_file in BOOKS_DIR.glob("*.md"):
        content = book_file.read_text(encoding="utf-8")
        book_id, _ = goodreads.read_book_id_and_image(content)
        if book_id:
            books_by_id.setdefault(book_id, []).append((book_file, content))

    removed_count = 0
    for book_id, file_data in books_by_id.items():
        if len(file_data) <= 1:
            continue

        # Keep the longest content (usually the more complete title/series info).
        file_data.sort(key=lambda entry: len(entry[1]), reverse=True)
        keep_file, keep_content = file_data[0]
        _, keep_image_path = goodreads.read_book_id_and_image(keep_content)
        keep_image_name = (
            pathlib.Path(keep_image_path).name if keep_image_path else None
        )

        for duplicate_file, duplicate_content in file_data[1:]:
            _, image_path = goodreads.read_book_id_and_image(duplicate_content)
            image_name = pathlib.Path(image_path).name if image_path else None
            if image_name == keep_image_name:
                image_path = None  # shared with the kept file; don't delete it

            goodreads.delete_book(duplicate_file, IMAGES_DIR, image_path)
            removed_count += 1
            print(
                f"Removed duplicate: {duplicate_file.stem} (same book_id as {keep_file.stem})"
            )

    if removed_count > 0:
        print(f"Removed {removed_count} duplicate books.")


def main() -> None:
    """Main entry point."""
    print("Fetching favorite books from Goodreads...")

    remove_skipped_books()
    remove_duplicate_books()

    books = fetch_goodreads_books()

    if not books:
        print("No favorite books found in feed.")
        remove_books_not_in_feed(set())
        return

    print(f"Found {len(books)} favorite books in feed.")

    remove_books_not_in_feed({book.book_id for book in books})

    created_count = 0
    updated_count = 0
    skipped_count = 0

    for book in books:
        success, action = process_book(book)
        if success:
            if action == "created":
                created_count += 1
            elif action == "updated":
                updated_count += 1
        else:
            skipped_count += 1

    print(
        f"\nCreated: {created_count}, Updated: {updated_count}, Skipped: {skipped_count}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fetch currently-reading books from Goodreads RSS feed."""

import pathlib
import sys
from dataclasses import dataclass

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

GOODREADS_FEED = "https://www.goodreads.com/review/list_rss/68793210?key=Q5sTrEOdYsUhUSrXK0J7wg9adkkcAuTFlIKN8-TetPnEWK2-&shelf=currently-reading"

SKIP_BOOK_IDS = {"29630264", "40186304", "32855235", "7930361160", "216017751"}

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT_DIR / "blog"
BOOKS_DIR = BLOG_DIR / "content/books/currently-reading"
IMAGES_DIR = BLOG_DIR / "assets/images/books/currently-reading"


@dataclass
class Book:
    title: str
    author: str
    slug: str
    goodreads_url: str
    book_id: str
    isbn: str
    image_url: str | None = None
    date_added: str | None = None


def build_front_matter(book: Book, image_path: str) -> str:
    """Build TOML front matter."""
    fields = {
        "title": book.title,
        "author": book.author,
        "draft": False,
        "goodreads_url": book.goodreads_url,
        "book_id": book.book_id,
        "isbn": book.isbn,
        "image": image_path,
    }

    if book.date_added:
        fields["date"] = book.date_added

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

        image_url = entry.get("book_large_image_url", "") or entry.get(
            "book_image_url", ""
        )
        image_url = image_url.strip() if image_url else None

        date_added = goodreads.parse_goodreads_date(
            entry.get("user_date_added", "").strip()
        )

        slug = slugify(f"{title}-{author}")

        books.append(
            Book(
                title=title,
                author=author,
                slug=slug,
                goodreads_url=goodreads_url,
                book_id=book_id,
                isbn=isbn,
                image_url=image_url,
                date_added=date_added,
            )
        )

    return books


def process_book(book: Book) -> bool:
    """Process a single book: download image and create content file."""
    image_url = book.image_url or get_image_url_from_sources(
        book.book_id, book.isbn, book.title, book.author
    )
    if not image_url:
        print(f"Skipping '{book.title}' - no image available")
        return False

    image_filename = determine_image_filename(book.slug, image_url)
    image_path_local = IMAGES_DIR / image_filename

    if not image_path_local.exists():
        try:
            download_image(image_url, image_path_local)
        except (requests.RequestException, OSError) as err:
            print(f"Failed to download image for '{book.title}': {err}")
            return False

    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    book_path = BOOKS_DIR / f"{book.slug}.md"
    image_path_relative = f"images/books/currently-reading/{image_filename}"

    front_matter = build_front_matter(book, image_path_relative)
    book_path.write_text(f"{front_matter}\n\n", encoding="utf-8")
    print(f"Saved: {book.title}")
    return True


def remove_skipped_books() -> None:
    """Remove existing books that are in the skip list."""
    removed = goodreads.remove_books_where(
        BOOKS_DIR, IMAGES_DIR, lambda book_id: book_id in SKIP_BOOK_IDS
    )
    if removed:
        print(f"Removed {removed} books from skip list.")


def remove_books_not_in_feed(books_in_feed: list[Book]) -> None:
    """Remove existing books that are not in the feed (and not in the skip list)."""
    keep_book_ids = {book.book_id for book in books_in_feed} | SKIP_BOOK_IDS
    removed = goodreads.remove_books_where(
        BOOKS_DIR, IMAGES_DIR, lambda book_id: book_id not in keep_book_ids
    )
    if removed:
        print(f"Removed {removed} books not in feed.")


def main() -> None:
    """Main entry point."""
    print("Fetching currently-reading books from Goodreads...")

    remove_skipped_books()

    books = fetch_goodreads_books()

    if not books:
        print("No books found in feed.")
        remove_books_not_in_feed([])
        return

    print(f"Found {len(books)} books in feed.")

    remove_books_not_in_feed(books)

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

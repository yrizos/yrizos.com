"""CLI and common utilities for fetching posts."""

import argparse
import json
import pathlib
import re
from datetime import datetime
from typing import Callable, Iterable, List, Optional
from urllib.parse import urlsplit, urlunsplit

import requests
from rich.console import Console
from rich.theme import Theme

from .blog_post import BlogPost

console = Console(theme=Theme(
    {"prompt": "bold cyan", "choice": "bold green", "error": "bold red"}))

DEFAULT_MEDIUM_FEED = "https://medium.com/feed/@yrizos"
DEFAULT_DEVTO_FEED = "https://dev.to/feed/yrizos"

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
BLOG_DIR = ROOT_DIR / "blog"
POSTS_DIR = BLOG_DIR / "content/writing"
IMAGES_DIR = BLOG_DIR / "assets/images/writing"
WEB_IMAGE_PREFIX = pathlib.Path("images/writing")


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
    from datetime import timezone
    from email.utils import parsedate_to_datetime

    value = raw_value or fallback
    if not value:
        raise ValueError(f"Post '{title}' is missing a publish date.")
    parsed = parsedate_to_datetime(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def build_front_matter(post: BlogPost, image_web_path: Optional[pathlib.Path]) -> str:
    """Create TOML front matter for the Hugo post."""
    fields = {
        "title": post.title,
        "date": post.date.isoformat(),
        "draft": False,
        "type": "posts",
        "canonical_url": post.original_url,
    }
    if image_web_path:
        fields["image"] = image_web_path.as_posix()
        fields["imageAlt"] = post.image_alt or ""
    if post.tags:
        fields["tags"] = post.tags
    if post.series_title:
        fields["series_title"] = post.series_title
    if post.series_order:
        fields["series_order"] = post.series_order

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
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    })
    
    if "medium.com" in url or "cdn-images-1.medium.com" in url:
        session.headers["Referer"] = "https://medium.com/"
    
    response = session.get(url, timeout=30)
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
    post_path.write_text(
        f"{front_matter}\n\n{post.markdown_body}\n", encoding="utf-8")


def prompt_for_post(post: BlogPost) -> str:
    """Prompt the user whether to import a specific post."""
    console.print(
        f"\n[choice]{post.title}[/choice]\n  Published: {post.date.strftime('%Y-%m-%d')}\n  URL: {post.original_url}"
    )
    while True:
        decision = console.input(
            "[prompt]Import this post? (yes/no/exit): [/prompt]").strip().lower()
        if decision in {"yes", "y"}:
            return "yes"
        if decision in {"no", "n"}:
            return "no"
        if decision in {"exit", "e"}:
            return "exit"
        console.print(
            "Please answer with 'yes', 'no', or 'exit'.", style="error")


def process_posts(posts: Iterable[BlogPost]) -> None:
    """Iterate through posts, prompting the user before writing each one."""
    for post in posts:
        decision = prompt_for_post(post)
        if decision == "exit":
            break
        if decision == "no":
            console.print(f"Skipping: {post.title}", style="choice")
            continue
        try:
            write_post(post)
            console.print(f"[green]Saved:[/green] {post.title}")
        except Exception as err:  # noqa: BLE001
            console.print(
                f"Failed to save '{post.title}': {err}", style="error")


def run(feed_fetcher: Callable[[str], List[BlogPost]], feed_url: str) -> None:
    """Fetch posts from the selected feed and process them."""
    posts = feed_fetcher(feed_url)
    if not posts:
        console.print("No posts found to process.", style="error")
        return
    process_posts(posts)


def main() -> None:
    """Main CLI entry point with argparse subcommands."""
    parser = argparse.ArgumentParser(
        description="Fetch posts from Medium or Dev.to")
    subparsers = parser.add_subparsers(
        dest="source", help="Source to fetch from")

    medium_parser = subparsers.add_parser(
        "medium", help="Fetch posts from Medium")
    medium_parser.add_argument(
        "--feed-url",
        default=DEFAULT_MEDIUM_FEED,
        help=f"Medium feed URL (default: {DEFAULT_MEDIUM_FEED})",
    )

    devto_parser = subparsers.add_parser(
        "devto", help="Fetch posts from Dev.to")
    devto_parser.add_argument(
        "--feed-url",
        default=DEFAULT_DEVTO_FEED,
        help=f"Dev.to feed URL (default: {DEFAULT_DEVTO_FEED})",
    )

    args = parser.parse_args()

    if not args.source:
        parser.print_help()
        return

    if args.source == "medium":
        from .fetch_medium import fetch_medium_posts

        run(fetch_medium_posts, args.feed_url)
    elif args.source == "devto":
        from .fetch_devto import fetch_devto_posts

        run(fetch_devto_posts, args.feed_url)

"""BlogPost data transfer object."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BlogPost:
    title: str
    slug: str
    date: datetime
    original_url: str
    markdown_body: str
    tags: list[str] = field(default_factory=list)
    image_url: str | None = None
    image_alt: str = ""
    series_title: str | None = None
    series_order: int | None = None

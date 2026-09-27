#!/usr/bin/env python3
"""CLI utility that fetches Medium or Dev.to posts and converts them into Hugo content files."""

import sys
from pathlib import Path

from posts import main

# Add scripts directory to path so we can import posts package
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))


if __name__ == "__main__":
    main()

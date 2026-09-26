# yrizos.com

Hugo-powered personal blog, built and served entirely through Docker so no local Hugo or Python install is required.

## Directory Structure

```text
.
├── .github/
│   └── workflows/
│       └── deploy-blog.yml    # GitHub Pages deployment workflow
├── blog/                      # Hugo site source containing content, layouts, and assets
│   ├── archetypes/            # Default front matter templates for new posts
│   ├── config/                # Environment-specific Hugo configuration files
│   ├── content/               # Markdown content files rendered into pages
│   ├── layouts/                # Hugo templates and partials that shape the site
│   ├── public/                 # Generated static output after building
│   ├── resources/              # Hugo cache and processed pipeline artifacts
│   ├── static/                 # Static assets (images, JS, CSS) served as-is
│   └── themes/                 # Theme packages pulled into the site
├── scripts/                    # Utility scripts that support the blog workflow
│   ├── fetch_posts.py          # CLI entry point for post fetching
│   ├── posts/                  # Post fetching package
│   │   ├── blog_post.py        # BlogPost data transfer object
│   │   ├── cli.py              # Common utilities and CLI
│   │   ├── fetch_medium.py     # Medium-specific fetching logic
│   │   └── fetch_devto.py      # Dev.to-specific fetching logic
│   ├── fetch_books.py          # Goodreads favorites import
│   ├── fetch_reading.py        # Goodreads currently-reading import
│   └── pdf_to_images.py        # PDF slide conversion to images
├── tests/                       # Pytest suite for the Python scripts
├── Dockerfile.python            # Docker image for Python scripts with dependencies
├── Makefile                     # Docker-based development commands
└── CNAME                        # Domain configuration used when deploying the site
```

## Local Development

The project includes a Makefile with Docker-based commands that don't require local Hugo installation.

Run `make help` at any time for the full command list.

### Development Server

Start the development server with drafts enabled:

```bash
make serve
```

Visit `http://localhost:1313/` to browse the site with live reload.

Other serve options:

- `make serve-future` - Include future-dated posts
- `make serve-prod` - Production-like server (no drafts)
- `make serve-clean` - Server without drafts
- `PORT=8080 make serve` - Use custom port

### Building

Build the site for development:

```bash
make build
```

Build for production:

```bash
make build-prod
```

Static site output goes to `blog/public/`.

### Other Commands

- `make clean` - Remove build artifacts
- `make help` - Show all available commands

### Pre-commit Hooks

Install [pre-commit](https://pre-commit.com/) and enable the repository hooks:

```bash
brew install pre-commit
pre-commit install --hook-type pre-commit
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

This installs checks for staged files, Conventional Commit messages, and signatures on commits being pushed.

The file checks include whitespace and conflict markers, YAML/TOML/JSON validation, large-file checks, Gitleaks secret scanning, Ruff for Python scripts, and actionlint for GitHub Actions workflows.

Run the checks on staged files manually:

```bash
pre-commit run
```

Run file hooks across all tracked files:

```bash
pre-commit run --all-files
```

## Content Import Scripts

All Python scripts run in Docker containers with dependencies pre-installed. The Docker image is built automatically on first use.

### Medium Posts

Fetches posts from Medium and converts them into Hugo-ready Markdown files.

```bash
make fetch-medium
```

Fetches from: https://medium.com/feed/@yrizos

### Dev.to Posts

Fetches posts from Dev.to and converts them into Hugo-ready Markdown files.

```bash
make fetch-devto
```

Fetches from: https://dev.to/feed/yrizos

### Goodreads Books

#### Favorite Books

Fetches favorite books from Goodreads RSS feed and creates Hugo content files.

```bash
make fetch-books
```

Fetches from: https://www.goodreads.com/review/list_rss/68793210?key=Q5sTrEOdYsUhUSrXK0J7wg9adkkcAuTFlIKN8-TetPnEWK2-&shelf=favorites

#### Currently Reading

Fetches currently-reading books from Goodreads RSS feed.

```bash
make fetch-reading
```

Fetches from: https://www.goodreads.com/review/list_rss/68793210?key=Q5sTrEOdYsUhUSrXK0J7wg9adkkcAuTFlIKN8-TetPnEWK2-&shelf=currently-reading

### PDF to Images

Converts PDF presentation slides to JPG images for use in talk pages.

```bash
make pdf-to-images PDF=path/to/presentation.pdf
```

## Testing

Run the Python test suite (also in Docker, dependencies included):

```bash
make test
```

## Deployment

Pushes to `main` that touch `blog/**` trigger the [`deploy-blog.yml`](.github/workflows/deploy-blog.yml) GitHub Actions workflow, which builds the Hugo site and publishes it to GitHub Pages.

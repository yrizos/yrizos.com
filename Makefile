# Hugo Blog Makefile

# Provides convenient Docker-based commands for Hugo development

# Variables
HUGO_VERSION := v0.151.2
HUGO_IMAGE := ghcr.io/gohugoio/hugo:$(HUGO_VERSION)
DOCKER_RUN := docker run --rm -v $(PWD):/app -w /app
VENV := .venv
PYTHON := $(VENV)/bin/python3

# Variables with defaults
PORT ?= 1313
ENV ?= development
DRAFTS ?= true

# Help target (default)
.PHONY: help
help:
	@echo "Hugo Blog Development Commands"
	@echo "============================="
	@echo ""
	@echo "Development:"
	@echo "  serve            - Start development server with drafts (default port 1313)"
	@echo "  serve-future     - Start development server with drafts and future posts"
	@echo "  serve-prod       - Start production-like server"
	@echo "  serve-clean      - Start server without drafts"
	@echo ""
	@echo "Building:"
	@echo "  build            - Build site for development"
	@echo "  build-prod       - Build site for production"
	@echo ""
	@echo "Utilities:"
	@echo "  hugo             - Run any hugo command (usage: make hugo -- --help)"
	@echo "  clean            - Clean build artifacts"
	@echo "  shell            - Open shell in hugo container"
	@echo ""
	@echo "Scripts:"
	@echo "  fetch-posts       - Fetch posts from Medium/Dev.to"
	@echo "  fetch-books        - Fetch 4 and 5 star read books from Goodreads RSS"
	@echo "  fetch-reading - Fetch currently-reading books from Goodreads"
	@echo "  venv-setup        - Set up Python virtual environment"
	@echo ""
	@echo "Parameters:"
	@echo "  PORT=8080        - Change server port (default: 1313)"
	@echo "  ENV=production   - Change environment (default: development)"
	@echo "  DRAFTS=false     - Disable drafts in serve commands"

# Development servers
.PHONY: serve
serve:
	@echo "Starting development server on port $(PORT)..."
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --buildDrafts --bind 0.0.0.0 --port $(PORT) --environment $(ENV)

.PHONY: serve-future
serve-future:
	@echo "Starting development server with future posts on port $(PORT)..."
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --buildDrafts --buildFuture --bind 0.0.0.0 --port $(PORT) --environment $(ENV)

.PHONY: serve-prod
serve-prod:
	@echo "Starting production-like server on port $(PORT)..."
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --environment production --bind 0.0.0.0 --port $(PORT)

.PHONY: serve-clean
serve-clean:
	@echo "Starting server without drafts on port $(PORT)..."
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --environment $(ENV) --bind 0.0.0.0 --port $(PORT)

# Building
.PHONY: build
build:
	@echo "Building site for development..."
	$(DOCKER_RUN) $(HUGO_IMAGE) --source blog --minify --cleanDestinationDir --gc --environment $(ENV)

.PHONY: build-prod
build-prod:
	@echo "Building site for production..."
	$(DOCKER_RUN) $(HUGO_IMAGE) --source blog --minify --cleanDestinationDir --gc --environment production

# Generic hugo command runner
.PHONY: hugo
hugo:
	@echo "Running hugo command..."
	$(DOCKER_RUN) -it $(HUGO_IMAGE) --source blog $(filter-out $@,$(MAKECMDGOALS))

# Prevent make from interpreting hugo arguments as targets
%:
	@:

# Utilities
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf blog/public blog/resources

.PHONY: shell
shell:
	@echo "Opening shell in hugo container..."
	$(DOCKER_RUN) -it --entrypoint /bin/sh $(HUGO_IMAGE)

# Show hugo version
.PHONY: version
version:
	@echo "Hugo version in container:"
	$(DOCKER_RUN) $(HUGO_IMAGE) version

# Validate hugo installation and config
.PHONY: check
check:
	@echo "Checking Hugo configuration..."
	$(DOCKER_RUN) $(HUGO_IMAGE) config --source blog

# Python virtual environment setup
.PHONY: venv-setup
venv-setup:
	@echo "Setting up Python virtual environment..."
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
	fi
	@echo "Installing dependencies..."
	@$(VENV)/bin/python3 -m pip install --upgrade pip --quiet
	@$(VENV)/bin/python3 -m pip install -r requirements.txt --quiet
	@echo "Virtual environment ready!"

# Scripts

.PHONY: fetch-posts
fetch-posts: venv-setup
	@echo "Fetching posts from Medium/Dev.to..."
	$(PYTHON) scripts/fetch_posts.py

.PHONY: fetch-books
fetch-books: venv-setup
	@echo "Fetching 4 and 5 star read books from Goodreads RSS..."
	$(PYTHON) scripts/fetch_books.py

.PHONY: fetch-reading
fetch-reading: venv-setup
	@echo "Fetching currently-reading books from Goodreads..."
	$(PYTHON) scripts/fetch_reading.py


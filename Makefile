# Hugo Blog Makefile

# Provides convenient Docker-based commands for Hugo development

# Variables
HUGO_VERSION := v0.151.2
HUGO_IMAGE := ghcr.io/gohugoio/hugo:$(HUGO_VERSION)
DOCKER_RUN := docker run --rm -v $(PWD):/app -w /app
PYTHON_IMAGE := python-scripts:latest
PYTHON_RUN := docker run --rm -it -v $(PWD):/app -w /app -e PYTHONUNBUFFERED=1 -e TERM=$(TERM) -e FORCE_COLOR=1 $(PYTHON_IMAGE)

# Colors
RESET := \033[0m
BOLD := \033[1m
GREEN := \033[32m
BLUE := \033[34m
CYAN := \033[36m
YELLOW := \033[33m

# Variables with defaults
PORT ?= 1313
ENV ?= development
DRAFTS ?= true

# Help target (default)
.PHONY: help
help:
	@echo "$(BOLD)$(CYAN)Hugo Blog Development Commands$(RESET)"
	@echo "$(CYAN)=============================$(RESET)"
	@echo ""
	@echo "$(BOLD)Development:$(RESET)"
	@echo "  $(GREEN)serve$(RESET)            - Start development server with drafts (default port 1313)"
	@echo "  $(GREEN)serve-future$(RESET)     - Start development server with drafts and future posts"
	@echo "  $(GREEN)serve-prod$(RESET)       - Start production-like server"
	@echo "  $(GREEN)serve-clean$(RESET)      - Start server without drafts"
	@echo ""
	@echo "$(BOLD)Building:$(RESET)"
	@echo "  $(GREEN)build$(RESET)            - Build site for development"
	@echo "  $(GREEN)build-prod$(RESET)       - Build site for production"
	@echo ""
	@echo "$(BOLD)Utilities:$(RESET)"
	@echo "  $(GREEN)hugo$(RESET)             - Run any hugo command (usage: make hugo -- --help)"
	@echo "  $(GREEN)clean$(RESET)            - Clean build artifacts"
	@echo "  $(GREEN)shell$(RESET)            - Open shell in hugo container"
	@echo ""
	@echo "Scripts:"
	@echo "  python-build     - Build Python Docker image with dependencies"
	@echo "  fetch-medium     - Fetch posts from Medium"
	@echo "  fetch-devto      - Fetch posts from Dev.to"
	@echo "  fetch-books      - Fetch favorite books from Goodreads RSS"
	@echo "  fetch-reading    - Fetch currently-reading books from Goodreads"
	@echo "  pdf-to-images    - Convert PDF slides to images"
	@echo ""
	@echo "$(BOLD)Parameters:$(RESET)"
	@echo "  $(YELLOW)PORT=8080$(RESET)        - Change server port (default: 1313)"
	@echo "  $(YELLOW)ENV=production$(RESET)   - Change environment (default: development)"
	@echo "  $(YELLOW)DRAFTS=false$(RESET)     - Disable drafts in serve commands"
	@echo "  $(YELLOW)PDF=path/to.pdf$(RESET)  - PDF file to convert (for pdf-to-images)"

# Development servers
.PHONY: serve
serve:
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --buildDrafts --bind 0.0.0.0 --port $(PORT) --environment $(ENV)

.PHONY: serve-future
serve-future:
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --buildDrafts --buildFuture --bind 0.0.0.0 --port $(PORT) --environment $(ENV)

.PHONY: serve-prod
serve-prod:
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --environment production --bind 0.0.0.0 --port $(PORT)

.PHONY: serve-clean
serve-clean:
	$(DOCKER_RUN) -p $(PORT):$(PORT) $(HUGO_IMAGE) serve --source blog --environment $(ENV) --bind 0.0.0.0 --port $(PORT)

# Building
.PHONY: build
build:
	$(DOCKER_RUN) $(HUGO_IMAGE) --source blog --minify --cleanDestinationDir --gc --environment $(ENV)

.PHONY: build-prod
build-prod:
	$(DOCKER_RUN) $(HUGO_IMAGE) --source blog --minify --cleanDestinationDir --gc --environment production

# Generic hugo command runner
.PHONY: hugo
hugo:
	$(DOCKER_RUN) -it $(HUGO_IMAGE) --source blog $(filter-out $@,$(MAKECMDGOALS))

# Prevent make from interpreting hugo arguments as targets
%:
	@:

# Utilities
.PHONY: clean
clean:
	rm -rf blog/public blog/resources

.PHONY: shell
shell:
	$(DOCKER_RUN) -it --entrypoint /bin/sh $(HUGO_IMAGE)

# Show hugo version
.PHONY: version
version:
	$(DOCKER_RUN) $(HUGO_IMAGE) version

# Validate hugo installation and config
.PHONY: check
check:
	$(DOCKER_RUN) $(HUGO_IMAGE) config --source blog

# Python Docker image
.PHONY: python-build
python-build:
	@if ! docker image inspect python:3.9-slim >/dev/null 2>&1; then \
		docker pull python:3.9-slim || (echo "Error: Failed to pull base image. Check your network connection."; exit 1); \
	fi
	docker build -f Dockerfile.python -t $(PYTHON_IMAGE) .

# Python scripts

.PHONY: fetch-medium fetch-devto
fetch-medium: python-build
	$(PYTHON_RUN) python scripts/fetch_posts.py medium

fetch-devto: python-build
	$(PYTHON_RUN) python scripts/fetch_posts.py devto

.PHONY: fetch-books
fetch-books: python-build
	$(PYTHON_RUN) python scripts/fetch_books.py

.PHONY: fetch-reading
fetch-reading: python-build
	$(PYTHON_RUN) python scripts/fetch_reading.py

.PHONY: pdf-to-images
pdf-to-images: python-build
	@if [ -z "$(PDF)" ]; then \
		echo "Error: PDF parameter is required"; \
		echo "Usage: make pdf-to-images PDF=path/to/presentation.pdf"; \
		exit 1; \
	fi
	$(PYTHON_RUN) python scripts/pdf_to_images.py $(PDF)


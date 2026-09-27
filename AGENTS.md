# AGENTS.md

This repository is a Hugo blog, built and served through Docker via the Makefile.
Before changing code, read `README.md` for commands, repository layout, and content-import instructions.

## Scope and precedence

When instructions conflict, use this order:
1. System/developer/user instructions.
2. This file.
3. Existing repository conventions and nearby code.
4. Generic best practices.

## Boundaries

Never:
- Never run `git reset --hard`.
- Never bypass commit signing (`--no-gpg-sign` or equivalent).
- Never add AI attribution to a commit message or PR description ("Generated with Claude Code," "Co-Authored-By: Claude," or similar).
- Never commit unless the user explicitly asked for a commit in the current turn.
- Never edit generated output directly: `blog/public/`, `blog/resources/`, `.ruff_cache/`.
- Never mix TOML and YAML front matter within one content section.
- Never invent front matter fields.
- Never hand-list books in `blog/content/reading/_index.md` — it is generated live from `currently-reading/`.
- Never automate, bypass, or auto-answer the yes/no/exit confirmation prompt in `make fetch-medium`, `make fetch-devto`, `make fetch-books`, or `make fetch-reading` — it is the only guard against duplicate or unwanted content.
- Never redeclare the HTML skeleton in a page template — `baseof.html` owns `header`/`main`/`footer`; page templates fill blocks only.
- Never rewrite runtime markup strings in `main.js` for state changes — toggle classes or swap icon names instead.
- Never put a global SCSS token or a literal value directly in a component rule body — use component variables (see SCSS component system).
- Never do arithmetic on a `_config.scss` global inside a component rule body (e.g. `$space-normal * 2`).

Always:
- Always check both `blog/layouts/` and `blog/themes/template/layouts/` before assuming a layout is single-sourced. `blog/layouts/` overrides the theme copy for site-specific behavior; edit the theme copy for the general case.
- Always keep commits signed (already configured — plain `git commit` signs automatically).
- Always use `git restore <file>` to discard a file's working-tree changes, or `git restore --staged <file>` to unstage, instead of `git reset --hard`. If a hard reset is explicitly requested, warn about permanent data loss and offer these two instead.

## Decision / stop rules

Proceed when the requested outcome and affected scope are clear from the request and repository context.

Ask before editing only when a blocking ambiguity would require guessing:
- multiple materially different interpretations of the requested behavior;
- unclear target/scope that repository inspection cannot resolve;
- conflicting requirements that instruction precedence cannot reconcile;
- a destructive or externally consequential action not explicitly authorized.

Do not ask merely because an implementation detail was left unspecified if existing code, tests, or repository conventions already determine it. A question gets an answer, not an implementation — information requests do not imply a request for code changes.

Scope discipline:
- Make the smallest change that satisfies the request.
- Do not add unrelated features, refactors, dependency updates, or speculative cleanup.
- Preserve existing behavior outside the requested change.

Literal interpretation:
- "Create a file" = create only that file, only the specified content.
- "Add a function" = add only that function.
- "Fix a bug" = fix only that bug.

## Verification

For every change:
1. Inspect the working tree before editing when useful.
2. Make the smallest change.
3. Run the most relevant tests/checks.
4. Before declaring the work complete, run `pre-commit run --all-files` (`.pre-commit-config.yaml` has the full hook list).
5. If committing, run this sequence immediately before the commit:
   1. `git status --short`
   2. `git diff`
   3. Read every modified file from disk, not from memory of the edit.
   4. Verify only intended changes remain — nothing changed by accident, nothing incomplete, nothing unrelated pulled in.
   5. Commit with a signed `git commit`.

The filesystem is the source of truth, not the chat history.

### Python scripts and tests

- Run `make test` after any change touching `scripts/` and before declaring that work complete, to confirm nothing broke.
- Every new function or behavior change in `scripts/` needs a corresponding new or updated test in `tests/`.
- Tests must never make real network/API calls (Goodreads, Medium, Dev.to, or any HTTP request) — mock them (e.g. `monkeypatch`, fakes/stubs), so the suite is deterministic and offline.

### Commit messages

Format:
```
type: imperative subject under 50 chars

- Describe the functional change.
- Add another bullet when needed.
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build` (whichever matches the primary change).

Rules:
- lowercase after the colon
- imperative mood (add/fix/change)
- no trailing period
- body always present, describes the functional change, NOT which files changed

Example — "Implement JWT token generation" is correct; "Add auth.js file" is wrong. "Add password validation" is correct; "Update user controller" is wrong.

Full example:
```bash
git status --short
git diff
# read every modified file
git commit -m "feat: add jwt authentication system

- Implement JWT token generation
- Add login and registration endpoints
- Add token refresh mechanism"
```

## Hugo / template conventions

- `baseof.html` owns the HTML skeleton with semantic landmarks (header, main, footer); child templates fill blocks only.
- Wrap page content in the shared container utility.
- Put reusable view logic in focused `_partials/`; document non-obvious inputs.
- Pass partial inputs explicitly, e.g. `dict "key" value` — never through globals.
- Use semantic markup: appropriate navigation elements; alt text on every image; machine-readable dates via `<time datetime="...">`; external links use `target="_blank" rel="noopener noreferrer"`.
- Design tokens for color, spacing, typography, and motion live in `_config.scss` only.
- Use Hugo Pipes for CSS/JS: unminified in development, minified/fingerprinted/cached in production.
- Reuse existing layout helpers and tokens; do not introduce ad hoc measurements.
- Render collections through shared list partials, pre-sorted before rendering, emitting human- and machine-readable metadata together.
- Interactive behavior belongs in `blog/themes/template/assets/js/main.js`. Guard every DOM lookup for a possibly-absent node.
- Use `{{-` / `-}}` to trim generated HTML whitespace.

Generic code-quality guidance (kept per instruction not to remove information, flagged as a cut candidate — research on agent context files finds this category doesn't measurably improve agent behavior since it's already implicit in model training, and it costs tokens on every read):
- Match existing code style and patterns in the file being edited.
- Add a comment only when intent is not obvious from the code itself.
- Validate inputs and handle edge cases; error messages must say what actually went wrong.
- Reuse existing utilities before writing new ones. Keep functions small and single-purpose. Avoid premature optimization.
- Test a change before calling it done.

## SCSS component system

Applies to `blog/themes/template/assets/css/_*.scss`, except `_config.scss`.

Every component file must follow this order:
1. Component variables at the top, grouped: Colors, Spacing, Sizes, Typography, Motion.
2. Variable values reference `_config.scss` globals only, or `lighten()`/`darken()` of them.
3. Rule bodies use component variables only (see Boundaries).

Exception: media-query breakpoints may reference global layout variables directly.

Naming: `$component-element-property` — e.g. `$series-number-bg`, `$series-items-gap`, `$series-number-font-size`, `$series-font-weight`, `$series-transition-duration`.

New component pattern:
```scss
// ============================================
// COMPONENT NAME
// ============================================

// Colors
$widget-bg: $color-background-primary;
$widget-text: $color-text-primary;

// Spacing
$widget-padding: $space-normal;

// Sizes
$widget-icon-size: $space-large;

// Typography
$widget-font-weight: $font-weight-normal;

// Motion
$widget-transition-duration: $motion-duration-normal;
$widget-transition-easing: $motion-easing-normal;

.widget {
  padding: $widget-padding;
  background: $widget-bg;
  color: $widget-text;
  transition: background-color $widget-transition-duration
    $widget-transition-easing;
}
```

When adding a partial, register its import in `main.scss` or it never renders.

Before finishing an SCSS change, verify: component variables are declared at the top; every one traces to a `_config.scss` global; rule bodies contain no raw literals or direct global references; naming follows `$component-element-property`.

## Front matter

Use exactly the format and fields defined for each section. Do not mix TOML and YAML within a section. Do not invent fields (see Boundaries).

- `blog/content/writing/*.md`
  - TOML
  - required: `title`, `date`, `draft`, `type="posts"`, `canonical_url`, `image`, `imageAlt`, `tags[]`
  - optional: `series_title`, `series_order`
- `blog/content/speaking/*.md`
  - YAML
  - required: `title`, `subtitle`, `date`, `draft`, `type="talk"`, `event`, `event_url`, `venue`, `slides_pdf`, `slides_dir`, `slide_count`, `image`, `tags`
  - optional: `co_presenter`
  - `slides_pdf` must already exist under `blog/static/slides/`
- `blog/content/books/recommendations/*.md`
  - TOML
  - required: `title`, `author`, `draft`, `goodreads_url`, `book_id`, `isbn`, `rating`, `image`, `date_read`, `tags`
- `blog/content/books/currently-reading/*.md`
  - TOML
  - required: same as recommendations except no `rating`; use `date` instead of `date_read`
- `blog/content/reading/_index.md`
  - only `title` (see Boundaries — never hand-list books here)

## Fast execution checklist

Before editing:
- Read `README.md` when repository context is needed.
- Identify the smallest affected surface.
- Check local patterns and relevant overrides.

After editing:
- Inspect the actual files on disk.
- Run targeted validation/tests.
- Run `pre-commit run --all-files`.
- Do not commit unless explicitly instructed.

# AGENTS.md

## Project

Hugo static blog migrated from Octopress. Theme: hugo-coder.

## Build

```bash
~/bin/hugo --minify
```

## Local dev server

```bash
~/bin/hugo server -D
```

## Lint/typecheck

Hugo build itself is the typecheck. A successful `hugo` build with zero errors is the validation.

```bash
~/bin/hugo --minify
```

## Deployment

- GitHub Pages via `.github/workflows/hugo.yaml` (auto-deploys on push to `main`)
- Docker: `podman build -t roadslesstaken .`

## Content

- Posts: `content/posts/*.md` (front matter: title, date, slug, categories, draft)
- Pages: `content/<section>/index.md` (about, smalltalk, spry, nim, ni, dart, evothings, messaging)
- Static assets: `static/` (images, pics, files, evothings, spry, ni, nim, etc.)
- Permalinks: `/:year/:month/:day/:slug/` (preserved from Octopress)

## Config

`hugo.toml` — baseURL is `https://gokr.github.io/roadslesstaken/`

## Theme

`themes/hugo-coder` (git submodule). Do not edit theme files directly. Override via `layouts/` overrides or `assets/` custom SCSS/CSS.

## Disqus

Shortname: `roadslesstaken`. Configured in `hugo.toml` under `[services.disqus]`.

## Key files

- `hugo.toml` — site config
- `migrate.py` — Octopress→Hugo migration script (reference only)
- `fix_shortcodes.py` — Octopress shortcode→markdown converter (reference only)
- `.github/workflows/hugo.yaml` — GitHub Pages deployment
- `Dockerfile` — container build

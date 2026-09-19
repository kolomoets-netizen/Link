# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **static HTML** project — Tilda landing-page blocks for a Russian-language tender-aggregation platform. There is **no package manager, no build step, no lint, and no automated tests**. There is nothing to install (the update script is effectively a no-op; Python 3 is preinstalled).

### Structure
- `tilda-landing/01-hero.html` … `07-crm-srm-kp.html` — standalone embeddable HTML blocks (inline `<style>`), pasted into Tilda's T123 HTML-code block. See `tilda-landing/README.md` for block order and customization.
- `tilda-landing/preview.html` — local preview that `fetch()`es the 7 block files; **requires an HTTP server** (browsers block `fetch` over `file://`).
- `tilda-landing/preview-standalone.html` and `docs/index.html` — all blocks inlined in one file; open directly in a browser, no server needed.
- `.github/workflows/pages.yml` — deploys the standalone preview to GitHub Pages on push.

### Run / preview (development)
- Full preview with separate blocks: `python3 -m http.server 8080` from the `tilda-landing/` directory, then open `http://localhost:8080/preview.html`. Serving from the repo root instead would require the URL `http://localhost:8080/tilda-landing/preview.html`, but the `fetch` paths are relative so serve from `tilda-landing/`.
- Quick check without a server: open `tilda-landing/preview-standalone.html` directly.

### Lint / test / build
- None exist. Do not add or expect these unless the task explicitly asks for them.

# AcpGram landing

URL: `/acpgram/`; source: `_build/acpgram_page.py`; generated file: `acpgram/index.html`.
Shared header/footer and language handling come from `_build/build.py` and `assets/site.js`.
Product layouts and behavior live in `acpgram/acpgram.css` and `acpgram/acpgram.js`.
The page is included in the regular site build so the daily workflow refreshes its HTML statistics fallback.

## Local preview and rebuild

```sh
python _build/acpgram_page.py
python -m http.server 8765
```

Open http://localhost:8765/acpgram/ (YouTube requires an HTTP referrer).
Opening `acpgram/index.html` directly from disk is also supported for layout, images, languages and the embedded statistics snapshot. Asset paths are relative; the live JSON fetch is skipped for `file://`. The YouTube player still requires the local HTTP server because YouTube does not accept a file URL as an HTTP referrer.
After adding Tailwind utility classes, run the standard CSS build:

```sh
python -c "import sys; sys.path.insert(0,'_build'); import build; build.build_css()"
```

The standard full rebuild is `python _build/build.py`. It also refreshes other site sections and their counters.

## Content verification

- Source: https://github.com/selesnow/acpgram (`README.md`, `src/engines.mjs`, `src/setup.mjs`, `src/bot.mjs`, `src/cli.mjs`).
- Separate Telegram tokens for separate installations give each machine its own bot and list of locally available engines. Access permissions may further restrict that list.
- Telegram topics require enabling topics in @BotFather; `/topics` switches modes and `/new` creates a dialog. Topics have separate project, engine and history.
- `src/bot.mjs` calls `getUpdates` with `timeout: 30`; setup calls `deleteWebhook`. No inbound port, public IP or webhook is required.
- Setup offers service installation, which starts the bot. When service installation is declined, the manual command is `acpgram`.
- API-key restriction is stated specifically for Claude Code Remote Control, rather than all remote access products: https://code.claude.com/docs/en/remote-control.
- No transcription or timecodes requested. Video poster changes to an inline 9:16 YouTube privacy-enhanced iframe on play. No YouTube iframe or connection before play with JavaScript enabled; the no-JS fallback is a lazy iframe.
- Content structure (2026-11 rewrite): hero (benefit + Install / Video) → when you need it → video → how it works (3 nodes) → 6 benefits → agents (what each needs) → install in 5 steps (agent tabs with "already installed" default and folded full install; one-line installer with OS tabs, OS preselected) → folded npm / source / Docker / service & updates → security with a practical tip → compact stats → FAQ → press → author → CTA. Section numbers "0N / ACPGRAM" removed.
- Agent install commands were checked against the official Claude Code setup documentation, OpenAI Codex README, Gemini CLI README and Antigravity CLI quickstart. Antigravity's official installers are under `https://antigravity.google/cli/`. Claude Code and Codex require separate ACP bridge packages. Docker includes engines and bridges in its image.
- AI Volna and Lord GPT links were confirmed by the owner; Habr: https://habr.com/ru/articles/1107278/.

## Images

Original SVG and original WebP remain intact in `img/acpgram/`. The logo has a lossless WebP variant and SVG fallback; the optimized hero has a JPEG fallback. OG images are 1200×630 in JPEG and WebP. The preview poster is local. All new images have dimensions and appropriate loading priority.
`prepare_acpgram_assets.py` uses Pillow and the rasterized logo PNG to reproduce raster assets. Runtime pages have no new package dependencies.

## Statistics and deployment prerequisite

The existing `.github/workflows/update-stats.yml` calls the existing site build, now including `_build/acpgram_stats.py`. Snapshot: `assets/acpgram-stats.json`; client fetch uses `no-store`, falling back to embedded HTML values.

Locally, the authenticated `gh` account can read `selesnow/acpgram/traffic/clones`. Initial stars, downloads, version and clone history were collected successfully. The snapshot contains no token.

**GITHUB_PAT is absent**: repository Actions secret names and variable names both returned empty lists. The local process also has no `GITHUB_PAT`, `GITHUB_TOKEN` or `GH_TOKEN` environment variable. The collector can use local `gh auth token` privately, matching the existing collector; Actions uses `GITHUB_PAT`, falling back to `GITHUB_TOKEN`. The automatic token for the site repository does not grant traffic access to the other repository.

Before relying on daily clone updates, add a repository Actions secret named `GITHUB_PAT` with access to `selesnow/acpgram` traffic statistics. Never put it into client code or JSON. Without it, public counters continue to update while the previous clone history stays intact and the Action reports a warning. `sourcesUpdated` records freshness for each source.

Clone history merges by calendar date, replaces overlapping daily buckets, preserves older buckets and computes a sum without double counting. Download totals use nonoverlapping yearly chunks from the npm creation date through yesterday. API 429 and 5xx responses are retried; API failures preserve previous values.

Manual `workflow_dispatch` has not been run: changes are intentionally not committed or pushed until the owner reviews them. After publication, run the existing Update package stats workflow and verify traffic access.

## Checks

- `python _build/test_acpgram_stats.py`: overlapping clone windows, corrections, old-history preservation and idempotence.
- `node --check acpgram/acpgram.js`.
- `_build/check_acpgram.cjs`: Chrome at 360/768/1280/1920 px, images, one H1, language switching, clipboard, keyboard tabs, inline video, reduced motion, no-JS content and `/acpgram` redirect.
- Browser tools are installed temporarily outside the repository in `%TEMP%/acpgram-tools`; screenshots and Lighthouse reports are in `%TEMP%/acpgram-qa`.
- Mobile Lighthouse before the installation-guide expansion: Performance **91**, Accessibility **100**, SEO **100**. The current audit scores are recorded in `_build/acpgram-checks.json`. Used headless Chrome with `--disable-gpu` (software rendering): a trace showed this Windows environment blocking its first frame while waiting for GPU presentation. With the default GPU path the earlier page scored 86 for Performance. This is a local audit, not a claim about production field data.
- Shared `changeLang()` skips its synchronous forced reflow only on `.acpgram-page`, where individual translated spans do not animate. Existing pages retain their behavior. Analytics on this landing loads on the first interaction or after 10 seconds; events are queued from page load. Section rendering is deferred off screen and reduced-motion preferences disable animations.

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
- 2026-11-20 (AcpGram 1.30): new sections after the 6 benefits — `projects` (new project from `/project`, `/files` for secrets bypassing the model, cloning a repository as a project) and `git` (6 cards: sign-in by link and code for GitHub and GitLab.com, own servers, changes and diff, save and push, branches and undo, publish and merge request; note on where the sign-in is stored). New section `news` after the stats: the first two entries of the `NEWS` list in `acpgram_page.py` plus a card linking to `/blog/?tag=acpgram#posts` — add a new blog post as a new entry on top of `NEWS`. Benefit cards mention the agent plan, quick-reply buttons, the message queue, the diff in edit requests, personal folders and `/usage`. Security has a note on personal workspaces and the Linux sandbox (`USER_WORKSPACES`, `AGENT_SANDBOX=bwrap`); FAQ has three new answers (teammates' projects, secrets, Git). Facts: README sections «Файлы проекта и секреты», «Git: GitHub и GitLab», «Личные пространства», «Песочница агента (Linux)».
- Agent install commands were checked against the official Claude Code setup documentation, OpenAI Codex README, Gemini CLI README and Antigravity CLI quickstart. Antigravity's official installers are under `https://antigravity.google/cli/`. Claude Code and Codex require separate ACP bridge packages. Docker includes engines and bridges in its image.
- AI Volna and Lord GPT links were confirmed by the owner; Habr: https://habr.com/ru/articles/1107278/.

## Documentation page

URL: `/acpgram/docs/`; source: `_build/acpgram_docs.py` and three Markdown files `_build/acpgram_docs/{ru,ua,en}.md`; generated file: `acpgram/docs/index.html`; layout and behavior: `acpgram/docs/docs.css`, `acpgram/docs/docs.js`.

- Every heading has an explicit id: `## Title {#id}` (section), `### Title {#id}` (subsection). The three files must have the same headings in the same order — the build stops and names the first difference. The id is the anchor shared by all languages (`/acpgram/docs/#git-signin`). Links between sections are written as `[text](#id)`; a link to a missing id stops the build.
- Screenshots: a line `{{shot: name | alt text}}` becomes a figure when `img/acpgram/docs/<name>.webp` (or `.png`, `.jpg`) exists and is skipped otherwise; `<name>.<lang>.webp` (`ru`, `ua`, `en`) overrides the picture for one language. The build prints the names that are still missing.
- Layout: screenshots stay outside the text, between its paragraphs, centred with their captions; screenshots that follow one another stand in a row (`segments()` in the generator, `.ad-figs` in `docs.css`). A click opens the full-size picture in a `<dialog>`. Sections end with previous / next links. The contents box is sticky (a bar under the site header on phones); it needs `overflow-x: clip` on `<body>` because the site hides horizontal overflow on both `<html>` and `<body>`. The search highlights matches in the text with the CSS Custom Highlight API; `/` focuses it. A side column for screenshots was tried and removed on the owner's request: pictures look better centred.
- Rebuild: `python _build/acpgram_docs.py` (also runs in `python _build/build.py`). Use the pinned versions from `_build/requirements.txt` (the page is rendered with Python-Markdown), otherwise the nightly workflow re-renders the page slightly differently.
- The landing links to the page from the hero, the install section and the final block (`DOCS` in `acpgram_page.py`); `sitemap.xml` has the address; the nightly workflow commits `acpgram/docs/index.html`.
- Facts: the AcpGram README (ru and en) and `src/i18n.mjs` for button labels in the three languages. In the bot's interface an agent is called an "engine" (ru «движок», uk «рушій»); the documentation says "agent" and explains this once in the `engine` section.

### AI chat on the documentation page

- A floating "Ask AI" button opens a chat window. Markup: `chat_html()` in `acpgram_docs.py`; behavior and styles: `acpgram/docs/chat.js`, `acpgram/docs/chat.css` (own classes `dc-*`, no Tailwind utilities).
- The backend is a Cloudflare Worker in `_worker/acpgram-docs-chat/` (see its `README.md`): it checks the origin and the limits, puts the whole documentation of the reader's language into the prompt and streams the answer of an OpenRouter free model. The worker address is `CHAT_API` in `acpgram_docs.py`. The OpenRouter key is a worker secret and never appears on the site.
- The build writes `acpgram/docs/docs.{ru,ua,en}.txt` — the Markdown sources without the screenshot lines. The worker fetches them from the site, so a documentation update needs only a rebuild and a push, not a worker deploy. `.txt`, because GitHub Pages turns `.md` files into HTML pages.
- The model is told to answer only from the documentation and to end with links like `[Title](#id)`; the page renders a small safe subset of Markdown and keeps only links to ids that exist on the page.
- The dialog lives in `sessionStorage` (`acpgramDocsChat`); nothing is stored on the server except request counters.
- Local check without a key: the worker `README.md`, section «Локальная проверка без ключа».

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

# DBMS Digest — Übersicht widget

A desktop panel showing the newest weekly digest (title + section headlines) on your Mac,
read straight from the local `digests/` folder. No network required.

## Install

1. **Install Übersicht** (a free desktop-widget host) if you don't have it:

   ```sh
   brew install --cask ubersicht
   ```

   …or download it from https://tracesof.net/uebersicht/ and drag it to Applications.
   Launch Übersicht once (it adds a menu-bar icon).

2. **Drop this widget into Übersicht's widgets folder.** Übersicht watches
   `~/Library/Application Support/Übersicht/widgets/`. Symlink this folder there so it stays
   in sync with the repo:

   ```sh
   ln -s "/Users/alena/dbms-digest/scripts/ubersicht/dbms-digest.widget" \
         "$HOME/Library/Application Support/Übersicht/widgets/dbms-digest.widget"
   ```

   (Copy instead of symlink if you prefer: `cp -R … "$HOME/Library/Application Support/Übersicht/widgets/"`.)

3. Übersicht picks it up automatically. If not, click the menu-bar icon → **Refresh All Widgets**.

## Using it

- **🏠 Home tab** — the 15 freshest items across all feeds (title + link), de-duplicated and
  capped per source so no single feed dominates.
- **Topic tabs** (Postgres / NoSQL / Distributed / Engines / Math) **× type sub-tabs**
  (Новости / Ресёрч / Компании / Личные / Статьи). Open a cell to see **up to 5 fresh headlines**
  pulled live from that cell's sources; if a feed is missing/offline it falls back to the curated
  **source list**. A small grey tag shows which source each headline came from.
- **Tags (pins)** — the chip row up top. Click a tag to **expand** its latest items
  (#planet, #news, #habr, #git-commits, #HN-db have live feeds → up to 15 items); tags without a
  feed (#pgsql-hackers, #pgsql-bugs, #pgsql-perf, #pgsql-events, #commitfest) just open the channel.
- **Research split:** in the *Ресёрч* sub-tab, mixed blogs are filtered by relevance — only
  DB/CS-research titles pass; personal posts stay under *Личные*. Tune `RESEARCH_RE` in the script.
- **Clicking needs focus on the desktop.** Übersicht widgets sit at desktop level, so first
  click an empty desktop spot (or use *Show Desktop*) so no app window is on top — then tabs and
  links respond. If a click does nothing, that's why.

## ✨ Claude summaries (via your subscription)

Every fresh item has a **✨** next to it. Click it and Claude reads the article and opens
a card with a 3–5 sentence summary aimed at a DBMS hacker, plus a link back to the original.

**No setup, no API key, no cost beyond your plan.** `summarize.py` calls the `claude` CLI that
ships inside the Cursor/VS Code **Claude Code extension** (`…/anthropic.claude-code-*/resources/
native-binary/claude`), which runs on your logged-in **Claude subscription** — not the paid API.
It's pure stdlib + that binary; the script auto-locates the newest extension version.

- Takes ~20–40 s per click (CLI startup + inference). Set `CLAUDE_MODEL = "haiku"` in
  `summarize.py` to make it faster, or `"sonnet"` / `"opus"` for the default of your choice.
- If the binary can't be found (extension missing / not logged in), clicking ✨ opens a card
  explaining that — it never fails silently.
- Wants the paid API instead? Earlier versions used the `anthropic` SDK + `ANTHROPIC_API_KEY`;
  the CLI path replaced it so you don't need credits.

## How it works / customizing

- The widget runs **`build_widget_items.py`**, which fetches each source's RSS/Atom feed
  (concurrently, ~10-25s first run), keeps the newest items per cell, builds the Home list, and
  **caches the result for ~90 min** so most refreshes are instant.
- **Curated sources, pins, tab names:** edit `widget-data.json`
  (`{ "t": "title", "u": "url" }`).
- **Add a live feed for a source:** add its homepage→feed URL to the `FEEDS` map in
  `build_widget_items.py`. Unknown/broken feeds are skipped silently (that cell then just shows
  source links).
- **Noisy feed in Home?** add it to `HOME_EXCLUDE` in the script (Qiita's firehose is already excluded).
- If your repo moves, fix the path in `command` (index.jsx) and `DATA` (the script).
- Position/size: `top` / `right` / `width` in the `className` block of `index.jsx`.
- Pair with the browser-homepage trick (`docs/latest.html`) for the full-text read of the current
  week — the widget is the *launcher*, `latest.html` is the *reader*.

> Note: `arxiv` (research) is empty on weekends — arXiv doesn't publish Sat/Sun; it fills on weekdays.

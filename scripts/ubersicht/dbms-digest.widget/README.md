# DBMS Digest — Übersicht desktop widget

A live desktop panel for PostgreSQL / DBMS news: topic tabs, expandable channel tags, and a
🏠 Home feed of the freshest items across dozens of sources — with one-click **Claude summaries**
that render inline, right in the widget.

It's a *launcher/reader*: each item is a link to the original; ✨ gives you a quick Russian
summary without leaving the desktop.

---

## What you need (prerequisites)

| For | Requirement |
|---|---|
| The widget itself | **macOS** + **Übersicht** (free desktop-widget host) |
| Fetching news | **python3** (3.8+; standard library only — nothing to `pip install`) |
| ✨ Claude summaries | The **Claude Code extension** for Cursor/VS Code, logged in with your **Claude subscription**. The widget reuses the `claude` CLI bundled inside it — **no API key, no credits**. |

Internet access is required (it pulls RSS/Atom feeds and scrapes a few pages).

---

## Install

1. **Install Übersicht** if you don't have it, and launch it once (menu-bar icon appears):
   ```sh
   brew install --cask ubersicht        # or download from https://tracesof.net/uebersicht/
   ```

2. **COPY the widget into Übersicht's widgets folder — do NOT symlink.**
   > ⚠️ A symlink breaks the widget's ES `import` (the module resolves from outside the widgets
   > dir) and the widget renders **blank**. Use a real copy.
   ```sh
   cp -R "$HOME/dbms-digest/scripts/ubersicht/dbms-digest.widget" \
         "$HOME/Library/Application Support/Übersicht/widgets/"
   ```

3. Übersicht picks it up automatically. If not: menu-bar icon → **Refresh All Widgets**.

**Only `index.jsx` lives as a copy.** The data + scripts (`build_widget_items.py`, `summarize.py`,
`widget-data.json`) are referenced by their absolute repo paths, so they run from the repo and need
no copying. **After editing `index.jsx` in the repo, re-copy it** to the widgets folder.

---

## Using it

- **🏠 Home** — the 15 freshest items across all feeds, de-duplicated, capped per source for variety.
- **Topic tabs** (Postgres / NoSQL / Distributed / Engines / Math) **× type sub-tabs**
  (Новости / Ресёрч / Компании / Личные / Статьи). A cell shows up to 15 fresh headlines from its
  sources (also capped per source); if no feed is available it falls back to the curated source list.
  A small grey tag shows each item's source.
- **Tags (pins)** — the chip row at the top. Click a tag to **expand** its latest items:
  - live: `#pgsql-hackers` `#pgsql-perf` (mailing lists), `#pgsql-bugs` `#commitfest` `#pgsql-events`
    (scraped from postgresql.org), `#planet` `#news` `#habr` `#git-commits` (GitHub commits),
    `#HN-db` (Hacker News via Algolia), `#arxiv-db`, `#substack` (CS/DB newsletters).
- **✨ summary** — next to every fresh item. Click it: a box opens under the item with a short
  Russian summary from Claude (with a **✕** to hide it). See below.
- **⟳** (header) — force an immediate fresh rebuild (clears the cache and refetches now).
- **☑ автообновление** (header) — toggle hourly auto-refresh on/off. On = everything refreshes
  every hour by itself; off = it stays put until you press ⟳.
- **Clicking needs desktop focus.** Übersicht widgets sit at desktop level — click an empty desktop
  spot first (or *Show Desktop*) so no window is on top, then tabs/links/buttons respond.

---

## ✨ Claude summaries (runs on your subscription)

Clicking ✨ runs `summarize.py`, which fetches the article and asks the **Claude Code CLI**
(`claude -p`) for a 3–5 sentence Russian summary, shown inline. It uses the `claude` binary bundled
in the Cursor/VS Code Claude Code extension — i.e. **your Claude subscription, not the paid API**, so
there's nothing to set up and each click costs nothing beyond your plan.

- It auto-locates the newest extension build (`~/.cursor/extensions/anthropic.claude-code-*/…/claude`).
- ~20–40 s per click (CLI startup + inference). Summaries run **only on click** — nothing is
  auto-summarized, so you don't spend on items you don't open.
- Model: edit `CLAUDE_MODEL` in `summarize.py` (`""` = subscription default, or `"haiku"` for speed).
- If the CLI isn't found / you're not logged in, the box shows a short note explaining it.

---

## How updates work

`index.jsx` re-runs `build_widget_items.py` on Übersicht's schedule (hourly). The script fetches all
feeds concurrently and **caches the result** so most ticks are instant:

- **☑ on:** the hourly tick refetches once the cache is older than ~55 min.
- **☐ off:** always serves the cache (no auto-refetch) until you press **⟳**.
- **⟳:** deletes the cache and rebuilds immediately.

The header shows **обновлено `<date> <time>`** — the real last-build time (updates on ⟳).

---

## Customizing

- **Sources / pins / tab names:** edit `widget-data.json` (each item `{ "t": "title", "u": "url" }`).
- **Add a live feed:** add a `homepage → feed` entry to the `FEEDS` map in `build_widget_items.py`.
  Broken/unknown feeds are skipped silently (the cell then shows source links).
- **Scraped channels (no RSS):** see `scrape_pg_list` / `scrape_pg_events` / `scrape_commitfest` /
  `scrape_hn` / `scrape_substack` and the `*_URLS` sets.
- **Noisy feed in Home:** add it to `HOME_EXCLUDE` (Qiita is already excluded).
- **Research relevance filter:** tune `RESEARCH_RE` in the script.
- **Size/position:** `width` / `top` / `right` in the `className` block of `index.jsx` (re-copy after).
- **Paths / portability:** every path derives from one parameter — `const BASE` at the top of
  `index.jsx`, defaulting to `$HOME/dbms-digest/scripts/ubersicht/dbms-digest.widget`. The shell
  expands `$HOME`, so **no username is hardcoded** and it works for any user whose repo is at
  `~/dbms-digest`. If your repo lives elsewhere, change that one line and re-copy. The daily
  LaunchAgent (`com.dbmsdigest.daily.plist`) runs through `bash -lc` so `$HOME` expands there too.
- **No secrets in the code.** No API keys or tokens are stored — ✨ uses the Claude Code CLI (your
  subscription), and nothing reads a key. Safe to publish.
- **Show on one monitor:** Übersicht's per-widget screen setting (menu-bar icon, or
  `~/Library/Application Support/tracesOf.Uebersicht/WidgetSettings.json` →
  `showOnAllScreens`/`showOnMainScreen`).

> The arXiv-backed cells & tabs (Math / AI / Algorithms, Ресёрч) are thin on weekends — arXiv doesn't publish Sat/Sun; they fill on weekdays.

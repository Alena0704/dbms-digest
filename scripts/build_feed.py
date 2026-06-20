#!/usr/bin/env python3
"""Build the published site + RSS feed from the weekly digests.

Reads every ``digests/YYYY-MM-DD.md`` file and emits, under ``docs/`` (served by
GitHub Pages):

* ``docs/feed.xml``            – RSS 2.0, one <item> per digest, full content inline
                                 (<content:encoded>), capped to MAX_ITEMS, stable GUID.
                                 Item links point at the in-site rendered page.
* ``docs/index.html``          – on-brand landing page: banner, subscribe, digest index
                                 linking to the in-site rendered pages (not GitHub).
* ``docs/digests/<date>.html`` – one rendered, on-brand page per digest, with a sticky
                                 left-column section menu (table of contents).

Run from the repo root:  python3 scripts/build_feed.py
No arguments. Safe to re-run; it fully regenerates everything each time.
"""

from __future__ import annotations

import datetime as dt
import html
import re
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

import markdown

# --- configuration ----------------------------------------------------------
SITE = "https://danolivo.github.io/dbms-digest"          # GitHub Pages site root
REPO = "https://github.com/danolivo/dbms-digest"         # source repo
FEED_TITLE = "DBMS Digest"
FEED_DESC = ("A weekly, ad-free, fact-checked roundup of PostgreSQL & wider DBMS "
             "internals, news, and research. Monday → Sunday.")
MAX_ITEMS = 26  # ~half a year of weekly digests; older ones stay in the archive

ROOT = Path(__file__).resolve().parent.parent
DIGESTS = ROOT / "digests"
DOCS = ROOT / "docs"
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")

# Shared on-brand styling (matches the banner: navy + amber).
CSS = """
    :root { --navy:#0d1b2e; --navy2:#13243a; --blue:#5a8bd4; --amber:#f5a623; --ink:#e7eef7; --mut:#8aa0bd; }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; background:var(--navy); color:var(--ink);
      font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
    a { color:var(--blue); }
    .wrap { max-width:760px; margin:0 auto; padding:24px 20px 64px; }
    .wrap.wide { max-width:1060px; }
    .banner img { width:100%; height:auto; border-radius:12px; display:block; }
    .sublabel { font-size:1.05rem; letter-spacing:.18em; text-transform:uppercase; color:var(--mut); margin:28px 0 4px; }
    p.lead { color:var(--ink); margin:0 0 20px; }
    .sub { display:inline-flex; align-items:center; gap:8px; background:var(--amber); color:var(--navy);
      font-weight:700; text-decoration:none; padding:11px 18px; border-radius:999px; }
    .sub:active { opacity:.85; }
    .feedurl { display:block; margin:14px 0 0; color:var(--mut); font-size:.85rem; word-break:break-all; }
    .feedurl code { color:var(--blue); }
    .index-h { font-size:.8rem; letter-spacing:.16em; text-transform:uppercase; color:var(--mut);
      border-top:1px solid var(--navy2); padding-top:24px; margin-top:36px; }
    ul.index { list-style:none; padding:0; margin:0; }
    ul.index li { border-bottom:1px solid var(--navy2); }
    ul.index li a { display:flex; gap:12px; align-items:baseline; padding:13px 4px; text-decoration:none; color:var(--ink); }
    ul.index li a:hover { color:var(--amber); }
    .date { color:var(--blue); font-variant-numeric:tabular-nums; font-weight:600; }
    .week { color:var(--mut); }
    .backlink { display:inline-block; margin:18px 0 8px; color:var(--blue); text-decoration:none; font-size:.9rem; }
    .backlink:hover { color:var(--amber); }
    footer { margin-top:40px; color:var(--mut); font-size:.85rem; border-top:1px solid var(--navy2); padding-top:18px; }
    footer a { color:var(--blue); }
    /* two-column digest layout with a sticky section menu */
    .layout { display:block; }
    nav.toc { display:none; }
    @media (min-width:980px) {
      .layout { display:grid; grid-template-columns:220px minmax(0,1fr); gap:44px; align-items:start; }
      nav.toc { display:block; position:sticky; top:24px; font-size:.85rem; }
    }
    nav.toc .toc-title { text-transform:uppercase; letter-spacing:.14em; font-size:.72rem; color:var(--mut); margin:0 0 10px; }
    nav.toc ul { list-style:none; padding:0; margin:0; }
    nav.toc li { margin:2px 0; border:0; }
    nav.toc a { display:block; padding:4px 10px; color:var(--mut); text-decoration:none;
      border-left:2px solid var(--navy2); line-height:1.35; }
    nav.toc a:hover { color:var(--amber); border-left-color:var(--amber); }
    /* rendered digest prose */
    .prose h1 { font-size:1.5rem; line-height:1.25; margin:8px 0 18px; color:var(--ink); }
    .prose h2 { font-size:.82rem; letter-spacing:.14em; text-transform:uppercase; color:var(--amber);
      border-top:1px solid var(--navy2); padding-top:22px; margin:34px 0 12px; scroll-margin-top:20px; }
    .prose p { margin:.5em 0 1em; }
    .prose ul { padding-left:1.2em; margin:.4em 0 1.2em; }
    .prose li { margin:.5em 0; }
    .prose li::marker { color:var(--mut); }
    .prose a { text-decoration:none; border-bottom:1px solid transparent; }
    .prose a:hover { color:var(--amber); border-bottom-color:var(--amber); }
    .prose strong { color:var(--ink); }
    .prose em { color:var(--mut); }
    .prose code { background:var(--navy2); color:#cfe0f5; padding:1px 5px; border-radius:4px; font-size:.92em; }
    .prose hr { border:0; border-top:1px solid var(--navy2); margin:28px 0; }
    .prose blockquote { margin:1em 0; padding:.4em 1em; border-left:3px solid var(--amber); color:var(--mut); }
"""


def digest_files() -> list[tuple[dt.date, Path]]:
    items = []
    for p in DIGESTS.glob("*.md"):
        m = DATE_RE.match(p.name)
        if not m:
            continue
        items.append((dt.date(int(m[1]), int(m[2]), int(m[3])), p))
    items.sort(key=lambda t: t[0], reverse=True)
    return items


def title_of(text: str, monday: dt.date) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    sunday = monday + dt.timedelta(days=6)
    return f"DBMS Weekly — week of {monday:%Y-%m-%d}–{sunday:%Y-%m-%d}"


def strip_leading_h1(text: str) -> str:
    """Drop the first H1 for the feed body (the reader shows the title separately)."""
    out, dropped = [], False
    for line in text.splitlines():
        if not dropped and line.startswith("# "):
            dropped = True
            continue
        out.append(line)
    return "\n".join(out).lstrip("\n")


def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["extra", "sane_lists"])


def rfc822(monday: dt.date) -> str:
    stamp = dt.datetime(monday.year, monday.month, monday.day, 12, 0, 0, tzinfo=dt.timezone.utc)
    return format_datetime(stamp)


def page_rel(monday: dt.date) -> str:
    return f"digests/{monday:%Y-%m-%d}.html"


def build_digest_page(monday: dt.date, path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    title = title_of(text, monday)
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
    body = md.convert(text)  # keeps the H1 and adds id slugs to every heading

    # Build a section menu from the level-2 headings.
    sections: list[tuple[str, str]] = []

    def walk(tokens):
        for t in tokens:
            if t["level"] == 2:
                sections.append((t["id"], t["name"]))
            walk(t.get("children", []))

    walk(md.toc_tokens)
    if sections:
        links = "\n".join(
            f'        <li><a href="#{i}">{html.escape(n)}</a></li>' for i, n in sections)
        toc = f'<nav class="toc"><p class="toc-title">Sections</p>\n      <ul>\n{links}\n      </ul>\n    </nav>'
    else:
        toc = ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · {html.escape(FEED_TITLE)}</title>
  <link rel="alternate" type="application/rss+xml" title="{html.escape(FEED_TITLE)}" href="../feed.xml">
  <style>{CSS}</style>
</head>
<body>
  <div class="wrap wide">
    <a class="backlink" href="../index.html">← All digests</a>
    <div class="layout">
    {toc}
      <article class="prose">
{body}
      </article>
    </div>
    <footer>
      <a href="../index.html">← All digests</a> ·
      <a href="../feed.xml">RSS feed</a> ·
      <a href="{REPO}/blob/main/digests/{path.name}">View source on GitHub</a>
    </footer>
  </div>
</body>
</html>
"""


def build_feed(items: list[tuple[dt.date, Path]]) -> str:
    now = format_datetime(dt.datetime.now(dt.timezone.utc))
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
        'xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        f"    <title>{escape(FEED_TITLE)}</title>",
        f"    <link>{SITE}/</link>",
        f"    <description>{escape(FEED_DESC)}</description>",
        "    <language>en</language>",
        f"    <lastBuildDate>{now}</lastBuildDate>",
        f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml" />',
    ]
    for monday, path in items[:MAX_ITEMS]:
        text = path.read_text(encoding="utf-8")
        title = title_of(text, monday)
        link = f"{SITE}/{page_rel(monday)}"  # in-site rendered page, not GitHub
        guid = f"dbms-digest-{monday:%Y-%m-%d}"
        content_html = md_to_html(strip_leading_h1(text))
        parts += [
            "    <item>",
            f"      <title>{escape(title)}</title>",
            f"      <link>{link}</link>",
            f'      <guid isPermaLink="false">{guid}</guid>',
            f"      <pubDate>{rfc822(monday)}</pubDate>",
            f"      <content:encoded><![CDATA[{content_html}]]></content:encoded>",
            "    </item>",
        ]
    parts += ["  </channel>", "</rss>", ""]
    return "\n".join(parts)


def build_index(items: list[tuple[dt.date, Path]]) -> str:
    rows = []
    for monday, path in items:
        sunday = monday + dt.timedelta(days=6)
        label = f"week of {monday:%b %-d}–{sunday:%b %-d}, {sunday:%Y}"
        rows.append(
            f'      <li><a href="{page_rel(monday)}">'
            f"<span class=\"date\">{monday:%Y-%m-%d}</span> "
            f"<span class=\"week\">{html.escape(label)}</span></a></li>")
    listing = "\n".join(rows) if rows else "      <li>No digests yet.</li>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(FEED_TITLE)}</title>
  <meta name="description" content="{html.escape(FEED_DESC)}">
  <link rel="alternate" type="application/rss+xml" title="{html.escape(FEED_TITLE)}" href="feed.xml">
  <style>{CSS}</style>
</head>
<body>
  <div class="wrap">
    <div class="banner"><img src="banner.jpg" alt="{html.escape(FEED_TITLE)} — a weekly roundup for internals developers &amp; database administrators."></div>

    <p class="sublabel">Subscribe</p>
    <p class="lead">{html.escape(FEED_DESC)}</p>
    <a class="sub" href="feed://danolivo.github.io/dbms-digest/feed.xml">\U0001F4E1 Subscribe via RSS</a>
    <span class="feedurl">Or paste this into your reader: <code>{SITE}/feed.xml</code></span>

    <p class="index-h">All digests</p>
    <ul class="index">
{listing}
    </ul>

    <footer>
      Generated from <a href="{REPO}">github.com/danolivo/dbms-digest</a>.
      Signal over sales.
    </footer>
  </div>
</body>
</html>
"""


def main() -> None:
    items = digest_files()
    DOCS.mkdir(exist_ok=True)
    (DOCS / "digests").mkdir(exist_ok=True)
    (DOCS / "feed.xml").write_text(build_feed(items), encoding="utf-8")
    (DOCS / "index.html").write_text(build_index(items), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    for monday, path in items:
        (DOCS / page_rel(monday)).write_text(build_digest_page(monday, path), encoding="utf-8")
    banner = ROOT / "pics" / "banner.jpg"
    if banner.exists():
        (DOCS / "banner.jpg").write_bytes(banner.read_bytes())
    print(f"Wrote feed.xml, index.html, and {len(items)} digest page(s) under docs/.")


if __name__ == "__main__":
    main()

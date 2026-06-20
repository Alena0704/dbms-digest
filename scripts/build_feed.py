#!/usr/bin/env python3
"""Build an RSS feed and a landing page from the weekly digests.

Reads every ``digests/YYYY-MM-DD.md`` file and emits:

* ``docs/feed.xml``  – RSS 2.0, one <item> per digest, full content inline
                       (<content:encoded>), capped to the most recent MAX_ITEMS,
                       with a stable GUID derived from the Monday date.
* ``docs/index.html`` – on-brand landing page with feed auto-discovery and a
                        subscribe link, served by GitHub Pages.

Run from the repo root:  python3 scripts/build_feed.py
No arguments. Safe to re-run; it fully regenerates both files each time.
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
REPO_BLOB = "https://github.com/danolivo/dbms-digest/blob/main"  # source files
FEED_TITLE = "DBMS Digest"
FEED_DESC = ("A weekly, ad-free, fact-checked roundup of PostgreSQL & wider DBMS "
             "internals, news, and research. Monday → Sunday.")
MAX_ITEMS = 26  # ~half a year of weekly digests; older ones stay in the archive

ROOT = Path(__file__).resolve().parent.parent
DIGESTS = ROOT / "digests"
DOCS = ROOT / "docs"
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")


def digest_files() -> list[tuple[dt.date, Path]]:
    """Return (monday_date, path) for every well-named digest, newest first."""
    items = []
    for p in DIGESTS.glob("*.md"):
        m = DATE_RE.match(p.name)
        if not m:
            continue
        d = dt.date(int(m[1]), int(m[2]), int(m[3]))
        items.append((d, p))
    items.sort(key=lambda t: t[0], reverse=True)
    return items


def title_of(text: str, monday: dt.date) -> str:
    """First level-1 heading, else a generated week label."""
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    sunday = monday + dt.timedelta(days=6)
    return f"DBMS Weekly — week of {monday:%Y-%m-%d}–{sunday:%Y-%m-%d}"


def strip_leading_h1(text: str) -> str:
    """Drop the first level-1 heading: the reader already shows the item title,
    so repeating it as an <h1> just wastes the top of the screen."""
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
    # noon UTC on the Monday — stable and unambiguous across readers
    stamp = dt.datetime(monday.year, monday.month, monday.day, 12, 0, 0,
                        tzinfo=dt.timezone.utc)
    return format_datetime(stamp)


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
        link = f"{REPO_BLOB}/digests/{path.name}"
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
            f'      <li><a href="{REPO_BLOB}/digests/{path.name}">'
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
  <link rel="alternate" type="application/rss+xml" title="{html.escape(FEED_TITLE)}" href="{SITE}/feed.xml">
  <style>
    :root {{ --navy:#0d1b2e; --navy2:#13243a; --blue:#5a8bd4; --amber:#f5a623; --ink:#e7eef7; --mut:#8aa0bd; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--navy); color:var(--ink);
      font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
    .wrap {{ max-width:760px; margin:0 auto; padding:24px 20px 64px; }}
    .banner img {{ width:100%; height:auto; border-radius:12px; display:block; }}
    h1 {{ font-size:1.05rem; letter-spacing:.18em; text-transform:uppercase; color:var(--mut); margin:28px 0 4px; }}
    p.lead {{ color:var(--ink); margin:0 0 20px; }}
    .sub {{ display:inline-flex; align-items:center; gap:8px; background:var(--amber); color:var(--navy);
      font-weight:700; text-decoration:none; padding:11px 18px; border-radius:999px; }}
    .sub:active {{ opacity:.85; }}
    .feedurl {{ display:block; margin:14px 0 0; color:var(--mut); font-size:.85rem; word-break:break-all; }}
    .feedurl code {{ color:var(--blue); }}
    h2 {{ font-size:.8rem; letter-spacing:.16em; text-transform:uppercase; color:var(--mut);
      border-top:1px solid var(--navy2); padding-top:24px; margin-top:36px; }}
    ul {{ list-style:none; padding:0; margin:0; }}
    li {{ border-bottom:1px solid var(--navy2); }}
    li a {{ display:flex; gap:12px; align-items:baseline; padding:13px 4px; text-decoration:none; color:var(--ink); }}
    li a:hover {{ color:var(--amber); }}
    .date {{ color:var(--blue); font-variant-numeric:tabular-nums; font-weight:600; }}
    .week {{ color:var(--mut); }}
    footer {{ margin-top:40px; color:var(--mut); font-size:.85rem; }}
    footer a {{ color:var(--blue); }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="banner"><img src="banner.jpg" alt="{html.escape(FEED_TITLE)} — a weekly roundup for internals developers &amp; database administrators."></div>

    <h1>Subscribe</h1>
    <p class="lead">{html.escape(FEED_DESC)}</p>
    <a class="sub" href="feed://danolivo.github.io/dbms-digest/feed.xml">\U0001F4E1 Subscribe via RSS</a>
    <span class="feedurl">Or paste this into your reader: <code>{SITE}/feed.xml</code></span>

    <h2>All digests</h2>
    <ul>
{listing}
    </ul>

    <footer>
      Generated from <a href="https://github.com/danolivo/dbms-digest">github.com/danolivo/dbms-digest</a>.
      Signal over sales.
    </footer>
  </div>
</body>
</html>
"""


def main() -> None:
    items = digest_files()
    DOCS.mkdir(exist_ok=True)
    (DOCS / "feed.xml").write_text(build_feed(items), encoding="utf-8")
    (DOCS / "index.html").write_text(build_index(items), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    # copy the banner next to the page so the Pages site is self-contained
    banner = ROOT / "pics" / "banner.jpg"
    if banner.exists():
        (DOCS / "banner.jpg").write_bytes(banner.read_bytes())
    print(f"Wrote {len(items[:MAX_ITEMS])} item(s) to docs/feed.xml and docs/index.html "
          f"({len(items)} digest(s) total).")


if __name__ == "__main__":
    main()

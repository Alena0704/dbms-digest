#!/usr/bin/env python3
"""Build the published site + RSS feed from the weekly digests.

Reads every ``digests/YYYY-MM-DD.md`` file and emits, under ``docs/`` (served by
GitHub Pages):

* ``docs/feed.xml``            – RSS 2.0, one <item> per digest, full content inline.
* ``docs/index.html``          – on-brand landing page (banner, subscribe, digest index).
* ``docs/digests/<date>.html`` – one rendered page per digest, with a sticky left-column
                                 section menu.
* SEO/discovery assets         – favicons, ``sitemap.xml``, ``robots.txt``,
                                 ``site.webmanifest``, plus per-page Open Graph / Twitter
                                 cards, canonical URLs, and JSON-LD structured data.

Run from the repo root:  python3 scripts/build_feed.py
No arguments. Safe to re-run; it fully regenerates everything each time.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

import markdown

# --- configuration ----------------------------------------------------------
# GitHub account + repo that publish this site. To run your own copy under a
# different account, set the env vars once (e.g. in your shell or CI):
#     DIGEST_OWNER=alena0704 python3 scripts/build_feed.py
# Everything below (feed URLs, canonical links, footer) is derived from these,
# so there's nothing else to change.
import os

OWNER = os.environ.get("DIGEST_OWNER", "danolivo")       # GitHub username
REPO_NAME = os.environ.get("DIGEST_REPO_NAME", "dbms-digest")

SITE = f"https://{OWNER.lower()}.github.io/{REPO_NAME}"   # GitHub Pages site root
REPO = f"https://github.com/{OWNER}/{REPO_NAME}"          # source repo
SITE_HOST = f"{OWNER.lower()}.github.io"                  # bare host for feed:// links
FEED_TITLE = "DBMS Digest"
SITE_TITLE = "DBMS Digest — weekly PostgreSQL & database internals roundup"
FEED_DESC = ("A weekly, ad-free, fact-checked roundup of PostgreSQL & wider DBMS "
             "internals, news, and research. Monday → Sunday.")
KEYWORDS = ("PostgreSQL, Postgres, database internals, DBMS, SQL, query optimizer, "
            "replication, MVCC, storage engine, database research, weekly digest, RSS")
MAX_ITEMS = 26  # ~half a year of weekly digests; older ones stay in the archive
FAVICONS = ["favicon.ico", "favicon-32.png", "apple-touch-icon.png", "icon-512.png"]

ROOT = Path(__file__).resolve().parent.parent
DIGESTS = ROOT / "digests"
DOCS = ROOT / "docs"
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")

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
    .site-title { font-size:1.6rem; margin:26px 0 8px; color:var(--ink); }
    .intro { color:var(--mut); margin:0 0 6px; font-size:1.02rem; line-height:1.6; }
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


def iso_noon(monday: dt.date) -> str:
    return dt.datetime(monday.year, monday.month, monday.day, 12, 0, 0,
                       tzinfo=dt.timezone.utc).isoformat()


def page_rel(monday: dt.date) -> str:
    return f"digests/{monday:%Y-%m-%d}.html"


def head_meta(title: str, desc: str, canonical: str, og_type: str, rel: str) -> str:
    """Shared SEO + favicon + social-card tags. `rel` prefixes asset paths
    ("" for the site root, "../" for pages under digests/)."""
    t, d = html.escape(title), html.escape(desc)
    return f"""<meta name="description" content="{d}">
  <meta name="keywords" content="{html.escape(KEYWORDS)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#0d1b2e">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="{rel}favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="{rel}favicon-32.png">
  <link rel="apple-touch-icon" href="{rel}apple-touch-icon.png">
  <link rel="manifest" href="{rel}site.webmanifest">
  <link rel="alternate" type="application/rss+xml" title="{html.escape(FEED_TITLE)}" href="{rel}feed.xml">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{html.escape(FEED_TITLE)}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/banner.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{SITE}/banner.jpg">"""


def jsonld(obj: dict) -> str:
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False) + "</script>")


PUBLISHER = {"@type": "Organization", "name": FEED_TITLE,
             "logo": {"@type": "ImageObject", "url": f"{SITE}/icon-512.png"}}


def build_digest_page(monday: dt.date, path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    title = title_of(text, monday)
    sunday = monday + dt.timedelta(days=6)
    canonical = f"{SITE}/{page_rel(monday)}"
    desc = (f"PostgreSQL & DBMS internals digest for the week of {monday:%b %-d}–"
            f"{sunday:%b %-d, %Y}: news, mailing lists, community pulse, commercial engines, "
            f"international sources, research, and conferences.")
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
    body = md.convert(text)

    sections: list[tuple[str, str]] = []

    def walk(tokens):
        for tk in tokens:
            if tk["level"] == 2:
                sections.append((tk["id"], tk["name"]))
            walk(tk.get("children", []))

    walk(md.toc_tokens)
    if sections:
        links = "\n".join(
            f'        <li><a href="#{i}">{html.escape(n)}</a></li>' for i, n in sections)
        toc = f'<nav class="toc"><p class="toc-title">Sections</p>\n      <ul>\n{links}\n      </ul>\n    </nav>'
    else:
        toc = ""

    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": title,
          "description": desc, "inLanguage": "en", "url": canonical,
          "mainEntityOfPage": canonical, "datePublished": iso_noon(monday),
          "dateModified": iso_noon(monday), "author": PUBLISHER, "publisher": PUBLISHER,
          "image": f"{SITE}/banner.jpg"}

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · {html.escape(FEED_TITLE)}</title>
  {head_meta(title, desc, canonical, "article", "../")}
  {jsonld(ld)}
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
        link = f"{SITE}/{page_rel(monday)}"
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
    blog_posts = [{"@type": "BlogPosting", "headline": title_of(p.read_text(encoding="utf-8"), m),
                   "url": f"{SITE}/{page_rel(m)}", "datePublished": iso_noon(m)}
                  for m, p in items[:MAX_ITEMS]]
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": FEED_TITLE,
          "url": f"{SITE}/", "description": FEED_DESC, "inLanguage": "en",
          "publisher": PUBLISHER, "blogPost": blog_posts}
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(SITE_TITLE)}</title>
  {head_meta(SITE_TITLE, FEED_DESC, f"{SITE}/", "website", "")}
  {jsonld(ld)}
  <style>{CSS}</style>
</head>
<body>
  <div class="wrap">
    <div class="banner"><img src="banner.jpg" alt="{html.escape(FEED_TITLE)} — a weekly roundup for internals developers &amp; database administrators."></div>

    <h1 class="site-title">DBMS Digest — weekly PostgreSQL &amp; database internals</h1>
    <p class="intro">A weekly, ad-free, fact-checked roundup of what actually happened in
    PostgreSQL and the wider database world: new internals and features, notable
    <code>pgsql-hackers</code>/<code>-bugs</code>/<code>-performance</code> threads, what the
    community argued about, real migration war stories, techniques from commercial engines
    (SQL Server, Oracle, MySQL, OceanBase), cutting-edge research, and upcoming conferences and
    CFPs. Built for database <strong>internals developers</strong> and DBAs who want signal, not
    marketing — roughly 15–25 scannable links per week, Monday → Sunday.</p>

    <p class="sublabel">Subscribe</p>
    <p class="lead">{html.escape(FEED_DESC)}</p>
    <a class="sub" href="feed://{SITE_HOST}/{REPO_NAME}/feed.xml">\U0001F4E1 Subscribe via RSS</a>
    <span class="feedurl">Or paste this into your reader: <code>{SITE}/feed.xml</code></span>

    <p class="index-h">All digests</p>
    <ul class="index">
{listing}
    </ul>

    <footer>
      Generated from <a href="{REPO}">github.com/{OWNER}/{REPO_NAME}</a>.
      Signal over sales.
    </footer>
  </div>
</body>
</html>
"""


def build_sitemap(items: list[tuple[dt.date, Path]]) -> str:
    today = dt.date.today().isoformat()
    newest = items[0][0].isoformat() if items else today
    urls = [f"  <url><loc>{SITE}/</loc><lastmod>{newest}</lastmod>"
            f"<changefreq>weekly</changefreq><priority>1.0</priority></url>"]
    for monday, _ in items:
        urls.append(f"  <url><loc>{SITE}/{page_rel(monday)}</loc>"
                    f"<lastmod>{monday.isoformat()}</lastmod>"
                    f"<changefreq>monthly</changefreq><priority>0.8</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main() -> None:
    items = digest_files()
    DOCS.mkdir(exist_ok=True)
    (DOCS / "digests").mkdir(exist_ok=True)
    (DOCS / "feed.xml").write_text(build_feed(items), encoding="utf-8")
    (DOCS / "index.html").write_text(build_index(items), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    for monday, path in items:
        (DOCS / page_rel(monday)).write_text(build_digest_page(monday, path), encoding="utf-8")

    # Stable "always newest" entry point. Set a browser homepage / Mac shortcut to this URL
    # (local file or the published site) and it always lands on the freshest digest.
    if items:
        newest = page_rel(items[0][0])
        (DOCS / "latest.html").write_text(
            '<!DOCTYPE html><meta charset="utf-8">'
            '<title>DBMS Digest — latest</title>'
            f'<meta http-equiv="refresh" content="0; url={newest}">'
            f'<link rel="canonical" href="{SITE}/{newest}">'
            f'<body style="font:16px system-ui;padding:2rem">Opening the latest digest… '
            f'<a href="{newest}">open it</a>.</body>', encoding="utf-8")

    # SEO / discovery assets
    (DOCS / "sitemap.xml").write_text(build_sitemap(items), encoding="utf-8")
    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (DOCS / "site.webmanifest").write_text(json.dumps({
        "name": FEED_TITLE, "short_name": FEED_TITLE, "description": FEED_DESC,
        "start_url": "./", "display": "browser",
        "background_color": "#0d1b2e", "theme_color": "#0d1b2e",
        "icons": [{"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # static assets copied from pics/ (no build-time image deps)
    for name, src in [("banner.jpg", ROOT / "pics" / "banner.jpg")] + \
                     [(f, ROOT / "pics" / f) for f in FAVICONS]:
        if src.exists():
            (DOCS / name).write_bytes(src.read_bytes())
    print(f"Wrote feed.xml, index.html, {len(items)} digest page(s), sitemap.xml, "
          f"robots.txt, manifest, and favicons under docs/.")


if __name__ == "__main__":
    main()

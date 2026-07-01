#!/usr/bin/env python3
"""Fetch up to 5 fresh items per widget cell and print the merged JSON.

The Übersicht widget runs this as its `command`. It:
  1. loads widget-data.json (topics × types × curated sources),
  2. for each source that has a known RSS/Atom feed, pulls the latest items,
  3. per cell, keeps the 5 newest items across that cell's feeds,
  4. prints widget-data.json with each cell turned into {sources, fresh},
  5. caches the result (~90 min) so most refreshes don't hit the network.

Pure stdlib. Any feed that errors / 404s is silently skipped (the cell then just
shows its curated source list). Safe to run anytime.
"""
from __future__ import annotations

import html
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
DATA = HERE / "widget-data.json"
CACHE = HERE / ".widget-live-cache.json"
FLAG_OFF = HERE / ".autorefresh-off"   # presence = hourly auto-refresh is OFF
CACHE_TTL = 90 * 60          # seconds
AUTO_TTL = 55 * 60           # auto-refresh ON: the hourly tick refetches once cache is older than this
PER_CELL = 15                # max fresh items shown per cell / pin
CELL_PER_SRC = 3             # per-cell: show at most N from one source first, for variety
HOME_N = 15                  # items on the Home tab
HOME_PER_SRC = 3             # cap per source on Home, so no single feed dominates
PER_FEED = 15                # items pulled from each feed before merging
TIMEOUT = 6                  # seconds per feed
UA = "Mozilla/5.0 (Macintosh) dbms-digest-widget/1.0"

# Map a source homepage (its `u` in widget-data.json) → its feed URL.
# Best-effort: unknown or broken feeds are skipped, so over-listing is harmless.
FEEDS = {
    "https://planet.postgresql.org/": "https://planet.postgresql.org/rss20.xml",
    "https://postgresweekly.com/": "https://postgresweekly.com/rss",
    "https://pganalyze.com/blog": "https://pganalyze.com/blog.rss",
    "https://www.postgresql.org/about/newsarchive/": "https://www.postgresql.org/news.rss",
    "https://habr.com/ru/hubs/postgresql/": "https://habr.com/ru/rss/hubs/postgresql/articles/?fl=ru",
    "https://habr.com/ru/hubs/nosql/": "https://habr.com/ru/rss/hubs/nosql/articles/?fl=ru",
    "https://arxiv.org/list/cs.DB/recent": "http://export.arxiv.org/api/query?search_query=cat:cs.DB&sortBy=submittedDate&sortOrder=descending&max_results=15",
    # arXiv topic searches: human search page (click-through) → dated API query (the feed).
    "https://arxiv.org/search/?searchtype=all&query=postgresql": "http://export.arxiv.org/api/query?search_query=cat:cs.DB+AND+all:postgresql&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/search/?searchtype=all&query=nosql": "http://export.arxiv.org/api/query?search_query=cat:cs.DB+AND+all:nosql&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/search/?searchtype=all&query=distributed+database": "http://export.arxiv.org/api/query?search_query=cat:cs.DB+AND+all:distributed&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/list/cs.LG/recent": "http://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/search/?searchtype=all&query=database+machine+learning": "http://export.arxiv.org/api/query?search_query=cat:cs.DB+AND+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/search/?searchtype=all&query=database+benchmark": "http://export.arxiv.org/api/query?search_query=all:benchmark+AND+cat:cs.DB&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/list/cs.LO/recent": "http://export.arxiv.org/api/query?search_query=cat:cs.LO&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/list/cs.DS/recent": "http://export.arxiv.org/api/query?search_query=cat:cs.DS&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/list/stat.ML/recent": "http://export.arxiv.org/api/query?search_query=cat:stat.ML&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://arxiv.org/list/math.NA/recent": "http://export.arxiv.org/api/query?search_query=cat:math.NA&sortBy=submittedDate&sortOrder=descending&max_results=15",
    "https://qiita.com/tags/postgresql": "https://qiita.com/tags/postgresql/feed",
    "https://www.crunchydata.com/blog": "https://www.crunchydata.com/blog/rss.xml",
    "https://www.enterprisedb.com/blog": "https://www.enterprisedb.com/blog/rss.xml",
    "https://www.timescale.com/blog": "https://www.timescale.com/blog/rss/",
    "https://stormatics.tech/": "https://stormatics.tech/feed",
    "https://blog.dalibo.com/": "https://blog.dalibo.com/feed.xml",
    "https://www.cybertec-postgresql.com/": "https://www.cybertec-postgresql.com/en/feed/",
    "https://hakibenita.com/": "https://hakibenita.com/feeds/all.atom.xml",
    "https://dev.to/franckpachot": "https://dev.to/feed/franckpachot",
    "https://thebuild.com/blog/": "https://thebuild.com/blog/feed/",
    "https://boringsql.com/": "https://boringsql.com/rss.xml",
    "https://dbmsmusings.blogspot.com/": "https://dbmsmusings.blogspot.com/feeds/posts/default",
    "https://muratbuffalo.blogspot.com/": "https://muratbuffalo.blogspot.com/feeds/posts/default",
    "https://blog.acolyer.org/": "https://blog.acolyer.org/feed/",
    "https://www.scylladb.com/blog/": "https://www.scylladb.com/blog/feed/",
    "https://redis.io/blog/": "https://redis.io/blog/feed/",
    "https://dbweekly.com/": "https://dbweekly.com/rss",
    "https://thenewstack.io/data/": "https://thenewstack.io/category/data/feed/",
    "https://www.percona.com/blog/": "https://www.percona.com/blog/feed/",
    "https://aws.amazon.com/blogs/database/": "https://aws.amazon.com/blogs/database/feed/",
    "https://duckdb.org/news/": "https://duckdb.org/feed.xml",
    "https://motherduck.com/blog/": "https://motherduck.com/rss.xml",
    "https://mariadb.org/": "https://mariadb.org/feed/",
    "https://www.cockroachlabs.com/blog/": "https://www.cockroachlabs.com/blog/index.xml",
    "https://www.yugabyte.com/blog/": "https://www.yugabyte.com/blog/feed/",
    # Russian PG-ecosystem vendors — via their Habr company blogs (no usable native RSS).
    "https://habr.com/ru/companies/postgrespro/articles/": "https://habr.com/ru/rss/companies/postgrespro/articles/?fl=ru",
    "https://habr.com/ru/companies/tantor/articles/": "https://habr.com/ru/rss/companies/tantor/articles/?fl=ru",
    "https://habr.com/ru/companies/arenadata/articles/": "https://habr.com/ru/rss/companies/arenadata/articles/?fl=ru",
    "https://habr.com/ru/companies/orion_soft/articles/": "https://habr.com/ru/rss/companies/orion_soft/articles/?fl=ru",
    # Apache Cloudberry (incubating) — PostgreSQL-based MPP warehouse, native blog feed.
    "https://cloudberry.apache.org/blog": "https://cloudberry.apache.org/blog/rss.xml",
    # StarRocks — MPP OLAP/analytics engine, native blog feed.
    "https://www.starrocks.io/blog/": "https://www.starrocks.io/blog/rss.xml",
    # Apache Iceberg — lakehouse table format; no blog RSS, use GitHub release notes.
    "https://github.com/apache/iceberg/releases": "https://github.com/apache/iceberg/releases.atom",
    # MySQL — Oracle blogs block RSS (403); use GitHub release notes instead.
    "https://github.com/mysql/mysql-server/releases": "https://github.com/mysql/mysql-server/releases.atom",
    # SPQR (pg-sharding) — PostgreSQL sharding router; follow commit activity.
    "https://github.com/pg-sharding/spqr": "https://github.com/pg-sharding/spqr/commits/master.atom",
    # ClickHouse — columnar OLAP DB; follow commit activity (no blog RSS).
    "https://github.com/ClickHouse/ClickHouse": "https://github.com/ClickHouse/ClickHouse/commits/master.atom",
    # WAL-G — PostgreSQL/MySQL backup & archival tool; follow commit activity.
    "https://github.com/wal-g/wal-g": "https://github.com/wal-g/wal-g/commits/master.atom",
    # pgconsul (Yandex) — PostgreSQL HA / automatic failover; follow commit activity.
    "https://github.com/yandex/pgconsul": "https://github.com/yandex/pgconsul/commits/main.atom",
    # Greengage — Greenplum fork (PostgreSQL-based MPP warehouse); follow commit activity.
    "https://github.com/GreengageDB/greengage": "https://github.com/GreengageDB/greengage/commits/main.atom",
    # Arenadata DB (arenadata/gpdb) — Greenplum-based MPP warehouse; follow commit activity.
    "https://github.com/arenadata/gpdb": "https://github.com/arenadata/gpdb/commits/master.atom",
    # Supabase — Postgres backend platform; native blog feed (higher-signal than repo commits).
    "https://supabase.com/blog": "https://supabase.com/rss.xml",
    # mailing lists via mail-archive.com — use the @lists.postgresql.org address (current).
    # The @postgresql.org address is the FROZEN pre-pglister archive (hackers stops at 2017,
    # bugs at 2013) — do NOT use it. pgsql-bugs has no working current feed, so it stays link-only.
    "https://www.postgresql.org/list/pgsql-hackers/": "https://www.mail-archive.com/pgsql-hackers@lists.postgresql.org/maillist.xml",
    "https://www.postgresql.org/list/pgsql-performance/": "https://www.mail-archive.com/pgsql-performance@lists.postgresql.org/maillist.xml",
    # pin-only channels (the tag row). #HN-db is handled via the Algolia JSON API (see scrape_hn).
    "https://git.postgresql.org/gitweb/?p=postgresql.git": "https://github.com/postgres/postgres/commits/master.atom",
}

# Feeds too noisy / low-signal for the Home digest (still shown in their own cell).
HOME_EXCLUDE = {
    "https://qiita.com/tags/postgresql/feed",
}

# Feeds whose every item counts as research (no keyword check needed).
ALWAYS_RESEARCH = {"http://export.arxiv.org/api/query?search_query=cat:cs.DB&sortBy=submittedDate&sortOrder=descending&max_results=15"}

# In the "research" sub-tab, mixed blogs (Murat, Abadi, Pachot…) are split by relevance:
# only DB/CS-research titles pass; personal posts ("Our Italy trip") are dropped from research
# (they still show under "personal"). arXiv items always pass.
RESEARCH_RE = re.compile(
    r"\b(database|databases|dbms|sql|postgres|postgresql|mysql|mariadb|duckdb|mongodb|oracle|"
    r"query|optimi[sz]|index|indexe?s|storage|transaction|isolation|serializ|consensus|"
    r"replicat|distribut|shard|partition|mvcc|b-?tree|lsm|vector|embedding|benchmark|latency|"
    r"throughput|schema|join|cardinalit|planner|\bwal\b|raft|paxos|oltp|olap|column|vacuum|"
    r"catalog|relational|graph|key-?value|\bkv\b|paper|proceedings|vldb|sigmod|cidr|icde|"
    r"spanner|cockroach|yugabyte|tidb|clickhouse|redis|cassandra|scylla)\b",
    re.I,
)


# strip XML namespaces so we can match by local tag name
def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _date(text: str) -> float:
    if not text:
        return 0.0
    text = text.strip()
    try:                       # RSS RFC-822
        return parsedate_to_datetime(text).timestamp()
    except Exception:
        pass
    try:                       # Atom ISO-8601
        from datetime import datetime
        return datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def _fmt_date(ts: float) -> str:
    """Unix ts → 'YYYY-MM-DD' (empty string if unknown)."""
    if not ts:
        return ""
    from datetime import datetime, timezone
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return ""


def _sub_for(feed_url: str, ts: float, author: str) -> str:
    """Build the small caption under an item: date, or 'author · date' for commit feeds."""
    d = _fmt_date(ts)
    if "/commits/" in (feed_url or "") and author:
        return f"{author} · {d}" if d else author
    return d


def fetch_feed(url: str):
    """Return list of (title, link, ts, author) for one feed, newest first; [] on any error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        raw = urllib.request.urlopen(req, timeout=TIMEOUT).read()
        root = ET.fromstring(raw)
    except Exception:
        return []

    out = []
    for el in root.iter():
        if _local(el.tag) not in ("item", "entry"):
            continue
        title = link = date = author = ""
        for c in el:
            ln = _local(c.tag)
            if ln == "title" and not title:
                title = (c.text or "").strip()
            elif ln == "link":
                href = c.get("href")
                if href:
                    link = href           # Atom
                elif c.text:
                    link = c.text.strip()  # RSS
            elif ln in ("pubdate", "published", "updated", "date") and not date:
                date = (c.text or "").strip()
            elif ln == "author" and not author:
                # Atom nests <name>; RSS puts text directly.
                nm = ""
                for cc in c:
                    if _local(cc.tag) == "name":
                        nm = (cc.text or "").strip()
                author = nm or (c.text or "").strip()
            elif ln == "creator" and not author:   # dc:creator (RSS)
                author = (c.text or "").strip()
        if title and link:
            out.append((title, link, _date(date), author))
        if len(out) >= PER_FEED:
            break
    return out


# Mailing lists that have no working RSS — scrape the official postgresql.org monthly
# archive (current month, falling back to previous) for fresh threads instead.
SCRAPE_LISTS = {
    "https://www.postgresql.org/list/pgsql-bugs/": "pgsql-bugs",
}
EVENTS_URL = "https://www.postgresql.org/about/events/"


def scrape_pg_events():
    """Return [{t,u,sub}] of upcoming community events from postgresql.org (sub = dates)."""
    try:
        req = urllib.request.Request(EVENTS_URL, headers={"User-Agent": UA})
        page = urllib.request.urlopen(req, timeout=TIMEOUT).read().decode("utf-8", "replace")
    except Exception:
        return []
    out, seen = [], set()
    # each event: <a href="/about/event/<slug>/">Title</a></div><div>Date: <dates></div>
    for href, title_html, date_html in re.findall(
            r'href="(/about/event/[^"]+)">(.*?)</a>\s*</div>\s*<div>\s*Date:\s*(.*?)</div>',
            page, re.S):
        title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", title_html))).strip()
        date = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", date_html))).strip()
        date = date.replace(" – ", "–")
        if not title or title.lower() in seen:
            continue
        seen.add(title.lower())
        out.append({"t": title, "u": "https://www.postgresql.org" + href, "sub": date})
        if len(out) >= PER_CELL:
            break
    return out


def scrape_pg_list(listname: str):
    """Return [(title, url)] of recent threads from postgresql.org's monthly archive."""
    t = time.gmtime()
    months = [(t.tm_year, t.tm_mon)]
    months.append((t.tm_year, t.tm_mon - 1) if t.tm_mon > 1 else (t.tm_year - 1, 12))
    out, seen = [], set()
    for (y, m) in months:
        url = f"https://www.postgresql.org/list/{listname}/{y:04d}-{m:02d}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            page = urllib.request.urlopen(req, timeout=TIMEOUT).read().decode("utf-8", "replace")
        except Exception:
            continue
        for href, txt in re.findall(r'href="(/message-id/[^"]+)"[^>]*>(.*?)</a>', page):
            title = html.unescape(re.sub(r"<.*?>", "", txt)).strip()
            base = re.sub(r"^((re:|\[[^\]]*\])\s*)+", "", title, flags=re.I)
            key = "".join(ch for ch in base.lower() if ch.isalnum())[:50]
            if not key or key in seen:
                continue
            seen.add(key)
            out.append((title, "https://www.postgresql.org" + href))
            if len(out) >= PER_CELL:
                return out
    return out


HN_URLS = {"https://hn.algolia.com/?query=postgres"}


def scrape_hn():
    """Return [(title, url, sub)] of recent HN Postgres stories via the Algolia API
    (more reliable than the hnrss bridge, which 502s often)."""
    api = ("https://hn.algolia.com/api/v1/search_by_date?tags=story&query=postgres"
           "&numericFilters=points%3E=10&hitsPerPage=25")
    try:
        req = urllib.request.Request(api, headers={"User-Agent": UA})
        data = json.loads(urllib.request.urlopen(req, timeout=TIMEOUT).read().decode("utf-8", "replace"))
    except Exception:
        return []
    out = []
    for h in data.get("hits", []):
        title = (h.get("title") or "").strip()
        if not title:
            continue
        link = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        pts = h.get("points")
        out.append((title, link, f"▲{pts}" if pts else ""))
        if len(out) >= PER_CELL:
            break
    return out


SUBSTACK_URLS = {"https://substack.com/"}
# CS + databases Substack newsletters (each has /feed). Broken ones are skipped.
SUBSTACK_FEEDS = [
    ("VuTrinh", "https://vutr.substack.com/feed"),
    ("ByteByteGo", "https://blog.bytebytego.com/feed"),
    ("Pragmatic Eng", "https://newsletter.pragmaticengineer.com/feed"),
    ("Data Eng Weekly", "https://www.dataengineeringweekly.com/feed"),
    ("Materialized View", "https://materializedview.io/feed"),
    ("Benn Stancil", "https://benn.substack.com/feed"),
]


def scrape_substack():
    """Merge several CS/DB Substack feeds, newest first, capped per source for variety."""
    rows = []
    for name, url in SUBSTACK_FEEDS:
        for (t, link, ts, _author) in fetch_feed(url):
            rows.append((ts, t, link, name))
    rows.sort(key=lambda r: r[0], reverse=True)
    out, per, seen = [], {}, set()
    for ts, t, link, name in rows:
        if link in seen or per.get(name, 0) >= CELL_PER_SRC:
            continue
        seen.add(link)
        per[name] = per.get(name, 0) + 1
        out.append({"t": t, "u": link, "src": name, "sub": _fmt_date(ts)})
        if len(out) >= PER_CELL:
            break
    return out


COMMITFEST_URLS = {"https://commitfest.postgresql.org/"}


def scrape_commitfest():
    """Return [(title, url)] of patches in the open CommitFest."""
    try:
        req = urllib.request.Request("https://commitfest.postgresql.org/current/",
                                     headers={"User-Agent": UA})
        page = urllib.request.urlopen(req, timeout=TIMEOUT).read().decode("utf-8", "replace")
    except Exception:
        return []
    out, seen = [], set()
    for href, txt in re.findall(r'href="(/patch/\d+/?)"[^>]*>(.*?)</a>', page, re.S):
        title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<.*?>", "", txt))).strip()
        if not title or title.lower() in seen:
            continue
        seen.add(title.lower())
        out.append((title, "https://commitfest.postgresql.org" + href))
        if len(out) >= PER_CELL:
            break
    return out


def short_src(title: str) -> str:
    t = title.split(" · ")[0].split(" — ")[0].split(" (")[0]
    for tag in ("[ru]", "[zh]", "[ja]", "[fr]", "[de]", "(new)"):
        t = t.replace(tag, "")
    return t.strip()[:18]


def main() -> None:
    auto_on = not FLAG_OFF.exists()
    age = (time.time() - CACHE.stat().st_mtime) if CACHE.exists() else 1e9
    # auto-refresh OFF → always serve cache (until a manual ⟳ clears it); ON → serve until AUTO_TTL.
    if CACHE.exists() and (not auto_on or age < AUTO_TTL):
        cached = json.loads(CACHE.read_text(encoding="utf-8"))
        cached["autorefresh"] = auto_on          # reflect the live flag, not the cached value
        print(json.dumps(cached, ensure_ascii=False))
        return

    data = json.loads(DATA.read_text(encoding="utf-8"))

    # Gather every feed we need, then fetch them all concurrently (fast).
    wanted = set()
    for topic in data.get("topics", []):
        for sources in topic.get("cells", {}).values():
            slist = sources if isinstance(sources, list) else sources.get("sources", [])
            for s in slist:
                f = FEEDS.get(s.get("u", ""))
                if f:
                    wanted.add(f)
    for p in data.get("pins", []):           # the tag row
        f = FEEDS.get(p.get("u", ""))
        if f:
            wanted.add(f)
    feed_cache: dict[str, list] = {}
    if wanted:
        with ThreadPoolExecutor(max_workers=12) as pool:
            for feed, items in zip(wanted, pool.map(fetch_feed, wanted)):
                feed_cache[feed] = items

    home = []  # global pool for the Home tab
    for topic in data.get("topics", []):
        cells = topic.get("cells", {})
        for type_id, sources in list(cells.items()):
            sources = sources if isinstance(sources, list) else sources.get("sources", [])
            merged = []
            for s in sources:
                feed = FEEDS.get(s.get("u", ""))
                if not feed:
                    continue
                src = short_src(s.get("t", ""))
                for title, link, ts, author in feed_cache.get(feed, []):
                    row = {"t": title, "u": link, "src": src, "_ts": ts, "_feed": feed,
                           "sub": _sub_for(feed, ts, author)}
                    merged.append(row)
                    if feed not in HOME_EXCLUDE:
                        home.append(row)
            # In "research", split mixed blogs by relevance: keep papers, drop personal posts.
            if type_id == "research":
                merged = [m for m in merged
                          if "export.arxiv.org" in m.get("_feed", "") or RESEARCH_RE.search(m["t"])]
            merged.sort(key=lambda x: x["_ts"], reverse=True)
            # Variety: take at most CELL_PER_SRC from one source first, then backfill with the
            # rest — so a prolific feed can't monopolize the top of the cell.
            diverse, extra, per = [], [], {}
            for m in merged:
                if per.get(m["src"], 0) < CELL_PER_SRC:
                    per[m["src"]] = per.get(m["src"], 0) + 1
                    diverse.append(m)
                else:
                    extra.append(m)
            ordered = diverse + extra
            fresh = [{"t": m["t"], "u": m["u"], "src": m["src"], "sub": m.get("sub", "")} for m in ordered[:PER_CELL]]
            cells[type_id] = {"sources": sources, "fresh": fresh}

    # Tags (pins): each pin with a feed gets up to PER_CELL fresh items.
    for p in data.get("pins", []):
        pu = p.get("u", "")
        if pu in SCRAPE_LISTS:                       # no RSS → scrape the official archive
            p["fresh"] = [{"t": t, "u": u} for (t, u) in scrape_pg_list(SCRAPE_LISTS[pu])]
            continue
        if pu == EVENTS_URL:
            p["fresh"] = scrape_pg_events()      # already [{t,u,sub}] with dates
            continue
        if pu in COMMITFEST_URLS:
            p["fresh"] = [{"t": t, "u": u} for (t, u) in scrape_commitfest()]
            continue
        if pu in HN_URLS:
            p["fresh"] = [{"t": t, "u": u, "sub": s} for (t, u, s) in scrape_hn()]
            continue
        if pu in SUBSTACK_URLS:
            p["fresh"] = scrape_substack()
            continue
        feed = FEEDS.get(pu)
        if not feed:
            continue
        items = sorted(feed_cache.get(feed, []), key=lambda x: x[2], reverse=True)
        fresh, seen = [], set()
        for t, u, _ts, _author in items:
            # collapse mailing-list threads: strip leading "Re:" / "[PATCH]" tokens, then key on subject
            base = re.sub(r"^((re:|\[[^\]]*\])\s*)+", "", t.strip(), flags=re.I)
            k = "".join(ch for ch in base.lower() if ch.isalnum())[:50]
            if k in seen:
                continue
            seen.add(k)
            fresh.append({"t": t, "u": u, "sub": _sub_for(feed, _ts, _author)})
            if len(fresh) >= PER_CELL:
                break
        p["fresh"] = fresh

    # Home: newest items across everything, de-duped by URL + title, capped per source.
    def _norm(s):
        return "".join(ch for ch in s.lower() if ch.isalnum())[:60]

    home.sort(key=lambda x: x["_ts"], reverse=True)
    seen_u, seen_t, per_src, home_top = set(), set(), {}, []
    for m in home:
        title = m["t"]
        # Planet-style "Author: Title" → also key on the part after the first colon,
        # so the same post via Planet and via the author's own feed collapses to one.
        keys = {_norm(title)}
        if ": " in title:
            keys.add(_norm(title.split(": ", 1)[1]))
        if m["u"] in seen_u or keys & seen_t:
            continue
        if per_src.get(m["src"], 0) >= HOME_PER_SRC:
            continue
        seen_u.add(m["u"]); seen_t |= keys
        per_src[m["src"]] = per_src.get(m["src"], 0) + 1
        home_top.append({"t": m["t"], "u": m["u"], "src": m["src"], "sub": m.get("sub", "")})
        if len(home_top) >= HOME_N:
            break
    data["home"] = home_top

    data["autorefresh"] = auto_on
    data["live_built"] = int(time.time())
    out = json.dumps(data, ensure_ascii=False)
    try:
        CACHE.write_text(out, encoding="utf-8")
    except Exception:
        pass
    print(out)


if __name__ == "__main__":
    main()

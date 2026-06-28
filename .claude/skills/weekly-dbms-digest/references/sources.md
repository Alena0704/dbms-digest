# Sources

The living source list for the weekly DBMS digest. Priority is a rough guide to scan order
(P1 = check every week, P2 = check most weeks, P3 = sample / opportunistic).
When you find a new high-signal source, append it under the right section with a one-line note
and a priority. When a source goes dormant or turns into pure marketing, mark it `[dormant]`
or `[mostly-marketing]` rather than deleting it, so it isn't re-added next week.

**Feed list:** the machine-readable RSS/Atom feeds scanned each run live in
`references/feeds.opml` (all languages; also importable into any feed reader). Keep it in sync
with this file — add confirmed feeds, drop dead ones.

## Aggregators & newsletters (start here — best fan-out)

- **Planet PostgreSQL** — official community blog aggregator; the firehose of core contributors, vendors, and independents. P1. https://planet.postgresql.org/
- **Postgres Weekly** — curated weekly Postgres newsletter (Cooperpress). Good signal, light on fluff. P1. https://postgresweekly.com/
- **DB Weekly** — broader weekly database newsletter (Cooperpress); covers the wider DBMS world. P1. https://dbweekly.com/
- **pganalyze "5mins of Postgres"** — weekly walkthrough of interesting Postgres content from the prior 7 days; effectively a pre-filtered digest. P1. https://pganalyze.com/blog
- **PostgreSQL News Archive** — official project announcements (releases, CVEs). P1. https://www.postgresql.org/about/newsarchive/
- **Hacker News (front page, db filter)** — sample for database/systems threads with real discussion. P2. https://hn.algolia.com/?query=postgres

## PostgreSQL blogs (primary)

- **Bruce Momjian** — core team; internals, community direction. P2. https://momjian.us/main/blogs/
- **Crunchy Data blog** — frequently substantive engineering (e.g. Elizabeth Christensen, Craig Kerstiens). Judge per-post; skip the pure product posts. P2. https://www.crunchydata.com/blog
- **pganalyze blog** — query performance, planner, internals. P2. https://pganalyze.com/blog
- **EDB blog** ("The Postgres Builders Blog") — enterprise Postgres, HA, migrations; filter heavily for marketing. P3. https://www.enterprisedb.com/blog · RSS https://www.enterprisedb.com/blog/rss.xml
- **Timescale blog** — time-series / analytics on Postgres; good patterns, watch for product push. P3. https://www.timescale.com/blog
- **Fujitsu (Fastware) Postgres blog** — internals and feature deep-dives. P3. https://www.postgresql.fastware.com/blog
- **Microsoft Azure for PostgreSQL blog** — sometimes solid internals; filter marketing. P3. https://techcommunity.microsoft.com/category/azuredatabases/blog/adforpostgresql
- **Postgres.ai blog** — DBLab, database branching, performance tooling. P3. https://postgres.ai/blog
- **Haki Benita** — high-quality, active PostgreSQL/SQL/Python performance deep-dives (row locking, ORM/planner pitfalls, "unconventional optimizations"). P2. https://hakibenita.com/
- **pgMustard blog** — Postgres query performance & EXPLAIN-plan analysis from the pgMustard team; low-volume but precise. No visible RSS → scan the HTML index. P2. https://www.pgmustard.com/blog

## PostgreSQL development (primary, highest trust)

- **pgsql-hackers mailing list** — where features are actually designed and argued. Highest signal for "what's coming". P1. https://www.postgresql.org/list/pgsql-hackers/
- **PostgreSQL commitfest** — patches under review; a roadmap of near-term features. P2. https://commitfest.postgresql.org/
- **PostgreSQL git commits** — ground truth for "did X actually land". Use to fact-check claims. P2. https://git.postgresql.org/gitweb/?p=postgresql.git
- **The Internals of PostgreSQL** (Hironobu Suzuki) — the authoritative internals reference: architecture, processes/memory, MVCC, vacuum, buffer manager, WAL/recovery, query processing, replication. Actively maintained (Async I/O chapter added Jun 2026). Not news — a fact-check / explainer resource when a thread or post makes an internals claim. P2 (reference). https://www.interdb.jp/pg/

## Wider DBMS & distributed data

- **Andy Pavlo / CMU DB Group blog** — industry analysis, annual "Databases in <year>" retrospective, seminar series. P1. https://www.cs.cmu.edu/~pavlo/blog/ and https://db.cs.cmu.edu/
- **DBMS Musings (Daniel Abadi)** — isolation/consistency, distributed DB theory made readable. P2. http://dbmsmusings.blogspot.com/
- **Murat Demirbas — Metadata blog** — distributed systems & database papers, paper reviews. P2. https://muratbuffalo.blogspot.com/
- **The New Stack — Databases** — news/trends; mixed, filter for substance. P3. https://thenewstack.io/data/
- **awesome-database-learning** — curated internals reading list; mine for new primary sources. P3. https://github.com/pingcap/awesome-database-learning
- **DoltHub blog** — engineering blog of Dolt (version-controlled SQL database) and Doltgres (Postgres-compatible variant); genuine storage/merge/diff and benchmarking internals, near-daily. **No RSS** — scan the HTML index directly (plain fetch works). P2. https://www.dolthub.com/blog/
- **DuckDB blog** — the embedded analytical (OLAP) engine; substantive engineering on vectorized execution, columnar storage, Iceberg/Parquet, releases & benchmarks. P2. https://duckdb.org/news/ · RSS https://duckdb.org/feed.xml
- **MotherDuck blog** — DuckDB-ecosystem (serverless DuckDB) engineering + product; good protocol/internals posts, filter the marketing. P3. https://motherduck.com/blog/ · RSS https://motherduck.com/rss.xml

## Commercial engines (new techniques & inventions — filter marketing hard)

- **SQL Server — Microsoft engineering blogs & docs** — "What's new" + engine internals; mine for real optimizer/storage/columnstore/Hekaton-style techniques, not feature sheets. P2. https://techcommunity.microsoft.com/category/sql-server/blog/sqlserver
- **Bob Ward / SQL Server team deep-dives** — internals talks and write-ups. P3. https://learn.microsoft.com/en-us/sql/
- **learn.microsoft.com — archived SQL Server engineering blogs** — static archive of old MSDN/TechNet SQL team blogs with deep query-execution/optimizer internals (e.g. bitmap filters, query processing). No new posts, but an excellent internals reference to cite/fact-check against. P3 (reference). https://learn.microsoft.com/en-us/archive/blogs/
- **Oracle Optimizer blog** — CBO internals and new optimizer features straight from the team. P2. https://blogs.oracle.com/optimizer/
- **Oracle Database Insider / Maria Colgan** — In-Memory, new-version internals. P3. https://blogs.oracle.com/database/
- **Chinar Aliyev's blog** `[dormant]` — deep Oracle CBO write-ups (cardinality estimation, hash-join performance, extended statistics). Inactive since 2021, but a solid archive reference for optimizer-internals claims. P3. https://chinaraliyev.wordpress.com/
- **Franck Pachot** — cross-engine internals (Oracle, Postgres, YugabyteDB, MongoDB); excellent technique-level comparisons. P2. https://dev.to/franckpachot
- **MySQL Server Blog / engineering** — InnoDB, optimizer, replication internals. P3. https://dev.mysql.com/blog-archive/
- **MariaDB Foundation** — the community MySQL fork; version previews (e.g. 13.1), optimizer/storage-engine (Aria, ColumnStore) news. Filter sponsor/PR posts. P3. https://mariadb.org/ · RSS https://mariadb.org/feed/
- **Percona blog (MySQL/Postgres/Mongo)** — often substantive engineering; filter the product posts. P3. https://www.percona.com/blog/

## Migration experience (real-world reports — prioritise)

- **AWS Database Blog — migrations** — Oracle/SQL Server → Postgres/Aurora war stories; technical, watch for product push. P2. https://aws.amazon.com/blogs/database/
- **Stormatics** — incident/migration field reports. P2. https://stormatics.tech/
- **pgEdge / Crunchy / EDB migration write-ups** — judge per-post for real lessons vs. pitch. P3.
- _Also surface migration posts that appear via Planet PostgreSQL and DB Weekly — they show up there regularly._

## Research venues (cutting edge — check for new proceedings / preprints)

- **VLDB** — proceedings (PVLDB). P2. https://www.vldb.org/pvldb/
- **SIGMOD / ACM SIGMOD Record** — major systems papers. P2. https://sigmod.org/
- **CIDR** — innovative/early systems ideas (e.g. Umbra). P2. https://www.cidrdb.org/
- **DBWorld (SIGMOD)** — CfPs and community announcements; useful to spot what's hot. P3. https://dbworld.sigmod.org/browse.html
- **arXiv cs.DB** — database preprints. P2. https://arxiv.org/list/cs.DB/recent
- **Hugging Face Papers (trending)** — ML preprint tracker; mostly LLM, but periodically surfaces DB-relevant work (vector/ANN search, learned indexes, NL→SQL, ML-driven query optimization, cardinality estimation). Sample only for DB-adjacent papers. P3. https://huggingface.co/papers/trending
- **ACM SIGMOD Record — current issue** — the quarterly DB-research bulletin (surveys, "industry perspectives", research highlights); ToC is public. Check once per quarter (Mar/Jun/Sep/Dec). P3. https://sigmodrecord.org/sigmod-record-current-issue/
- **The VLDB Journal (Springer)** — the flagship database journal; abstracts/ToC are public even though full text is paywalled. Scan the latest-articles ToC for new internals/optimizer/storage work. P3. https://link.springer.com/journal/778
- **The Morning Paper (Adrian Colyer)** `[dormant]` — random walk through CS research with superb plain-language paper reviews (DB isolation, consensus, storage). Ended Feb 2021, but the archive is a goldmine for understanding a cited paper. P3. https://blog.acolyer.org/

**Research discovery tools** (not weekly scans — use these to *find / fact-check the primary paper* behind a claim, querying `cs.DB`-style terms; CS-strong ones first):
- **Semantic Scholar** — AI-powered academic search, strong CS coverage, has an API. https://www.semanticscholar.org/
- **CORE** — largest aggregator of open-access papers (full-text + API). https://core.ac.uk/
- **BASE** — Bielefeld OA search engine. https://www.base-search.net/
- **DOAJ** — Directory of Open Access Journals (find legitimate OA DB venues). https://doaj.org/
- _Skip for this digest_: PubMed/PLOS (biomedical/life-sciences), SSRN (econ/law), WorldWideScience (broad federated science) — off-topic for DBMS; Google Scholar works only as ad-hoc search, not a scan.

## Conferences & CFP trackers (for the Call-for-papers section)

Find conferences / PGDays / meetups with an **open** CFP, plus applied/research venues close to
Postgres. List a CFP only while its deadline is in the future.

**PostgreSQL community events**
- **PostgreSQL.org — Upcoming events** — official community event list. P1. https://www.postgresql.org/about/events/
- **PostgreSQL.org — News archive** — "CFP is now open" announcements land here. P1. https://www.postgresql.org/about/newsarchive/
- **dev.events — Postgres** — aggregator of Postgres conferences with dates/CFPs. P2. https://dev.events/postgres
- **PGConf.dev** — the developers' conference. P2. https://www.pgconf.dev/
- **PGConf.EU** — European community conference (year-versioned site). P2. https://www.pgconf.eu/
- _Regional PGDays_: Nordic PGDay, PGDay Paris, PGDay Boston, PGDay UK / Lowlands, PGDay Israel, FOSDEM PGDay, Prague PostgreSQL Developer Day (p2d2.cz), Swiss PGDay, PGConf NYC / India. P3.

**Applied & research DB-systems venues (close to Postgres)**
- **VLDB** — rolling monthly PVLDB research deadlines. P2. https://www.vldb.org/
- **ACM SIGMOD** — multi-round research deadlines (year-versioned site). P2. https://sigmod.org/
- **CIDR** — innovative/early systems ideas. P2. https://www.cidrdb.org/
- **IEEE ICDE** — https://icde.org/ . P3.
- **DEBS** — distributed & event-based systems. https://debs.org/ . P3.
- **USENIX ATC / OSDI** — systems venues with frequent DB work. https://www.usenix.org/conferences . P3.
- **WikiCFP — databases** — academic CFP aggregator. http://www.wikicfp.com/cfp/call?conference=databases . P3.
- _Practitioner_: P99 CONF, HYTRADBOI. P3.

## Non-English sources (multilingual)

_Scan these in their native language and present items per the non-English formatting rule
(English headline + one-liner, a language tag, original title in parentheses). The same
anti-marketing and fact-check bar applies — verify technical claims against the original, not
just a translation._

_Prefer each source's RSS/Atom feed where available (dated, language-native, fetches cleanly).
For JS-heavy or region-specific sites that return stale/empty HTML — Chinese aggregators
(modb.pro), PolarDB / Alibaba Cloud, PingCAP, also Reddit and Qiita — render them with the
Claude-in-Chrome browser tools instead of a plain fetch. Treat web search as English/US-biased:
use it to confirm, not to discover._

### Russian `[ru]`
- **Postgres Pro blog** — Russian Postgres vendor; internals, patches, version deep-dives (some cross-posted in EN). P2. https://postgrespro.ru/blog
- **Habr — PostgreSQL hub** — large RU dev community; internals posts and production war stories. `[js]` P2. https://habr.com/ru/hubs/postgresql/
- **CITForum — Данные/СУБД** — long-running RU IT library (since 1997); mostly an *archive* of classic DB theory (Codd, relational model, translated papers) rather than weekly news. Use as a reference for fundamentals; site still updates but rarely with fresh internals. P3 (reference). https://citforum.ru/database/

### Chinese `[zh]`
- **PingCAP / TiDB blog (CN)** — distributed SQL internals, Raft, TiKV. P2. https://cn.pingcap.com/blog/
- **OceanBase** — distributed DB engineering write-ups (CN). P3. https://www.oceanbase.com/
- **Alibaba Cloud developer (PolarDB / AnalyticDB)** — engine internals; huge, filter hard. `[js]` P3. https://developer.aliyun.com/
- **modb.pro (墨天轮)** — Chinese DBA community and articles (Oracle, PG, MySQL, domestic engines). P3. https://www.modb.pro/

### French `[fr]`
- **Dalibo blog** — French Postgres consultancy; substantive internals (FR, some EN). P2. https://blog.dalibo.com/ · RSS https://blog.dalibo.com/feed.xml
- **dbi-services blog** — Swiss; PG/Oracle/SQL Server ops (FR + EN). P3. https://www.dbi-services.com/blog/

### German `[de]`
- **Cybertec (DE)** — German-language posts from the Cybertec team (the EN edition is listed above). P3. https://www.cybertec-postgresql.com/de/

### Japanese `[ja]`
- **Qiita — PostgreSQL tag** — large JP dev community; how-tos and internals. `[js]` P3. https://qiita.com/tags/postgresql · RSS https://qiita.com/tags/postgresql/feed
- **SRA OSS (JP)** — Japanese Postgres support company write-ups. P3. https://www.sraoss.co.jp/

_Discover more per the self-update rule — pin precise regional blogs/authors/channels
(incl. Telegram, WeChat, Qiita) as you find keepers; retire dead ones._

## New sources added (log)

_Append discoveries here with date, name, link, and a one-line reason. Example:_
- (2026-06-18) _seed list created._
- (2026-06-18) boringsql.com (Radim Marek) — reproducible Postgres internals deep-dives. https://boringsql.com/
- (2026-06-18) justatheory.com (David Wheeler) — PGXN/extensions + Postgres↔ClickHouse interop. https://justatheory.com/
- (2026-06-18) stormatics.tech — incident-style Postgres ops deep dives. https://stormatics.tech/
- (2026-06-18) thebuild.com (Christophe Pettus) — near-daily GUC-internals series and cross-engine planner deep-dives. P2. https://thebuild.com/blog/
- (2026-06-18) event-driven.io (Oskar Dudycz) — event sourcing / Postgres-as-event-store engineering. P3. https://event-driven.io/
- (2026-06-18) modern-sql.com (Markus Winand) — cross-engine SQL-standard conformance and feature comparisons. P2. https://modern-sql.com/
- (2026-06-22) pghackers.com — AI-assisted search/explorer over the pgsql-hackers archive; trial as a faster way to triage in-window threads than the raw monthly index. P3. https://www.pghackers.com/
- (2026-06-28) EDB blog RSS added to feeds.opml — https://www.enterprisedb.com/blog/rss.xml (plain-fetch [ok]); marketing-heavy, filter hard.
- (2026-06-28) Batch triage of a reader-submitted source list. **Added:** interdb.jp (PG Internals reference), dolthub.com/blog (versioned-SQL internals, no RSS → HTML scan), learn.microsoft.com/archive/blogs (SQL Server internals archive), chinaraliyev.wordpress.com (Oracle CBO archive `[dormant]`), huggingface.co/papers/trending (DB-adjacent ML, P3). **Skipped** (re-evaluate only if they change): habr.com bare site (already covered by the PostgreSQL-hub feed); huggingface root (covered by the trending page); runebook.dev (docs mirror, no original content); datacadamia.com (personal wiki notes, not news); math.stackexchange.com (off-topic); baeldung.com/cs (Java-centric, rarely DB); afteracademy.com (generic CS edu); programmersought.com (machine-translated SEO scrape); jianshu.com (too broad, no DB focus); cnblogs.com/gaojian (Python basics, not DB); mdpi.com/journal/mathematics (not DB-focused; MDPI quality concerns); academia.edu (paper-sharing platform, no clean feed); packtpub.com (mostly book promo — only the rare author interview qualifies; surface via search, not a scan); thewikihow.com/digest (CMU-DB aggregator looks useful but returns HTTP 403 to plain fetch — revisit via browser). **Already in use:** mail-archive.com/pgsql-hackers (the existing mailing-list fetch path).
- (2026-06-28) Second reader batch. **Added:** hakibenita.com (active PG/SQL perf, P2), pgmustard.com/blog (PG EXPLAIN/perf, P2, HTML scan), sigmodrecord.org current issue (quarterly, P3), link.springer.com/journal/778 = The VLDB Journal (ToC public, P3), blog.acolyer.org "The Morning Paper" (`[dormant]` paper-review archive, P3), citforum.ru/database (RU classic-DB-theory archive, P3). **Skipped:** kitchingroup.cheme.cmu.edu (chemistry/Emacs), physics.stackexchange.com (off-topic), academia.edu/IjdmsAircc (AIRCC/IJDMS low-tier journal on a paper-sharing platform), adtmag.com + infoworld.com + visualstudiomagazine.com (general/.NET tech news, low DB density, marketing-leaning), onlinelibrary.wiley.com/journal/5192 (paywalled HTTP 402, unidentifiable), link.springer.com broad discipline searches (paywalled firehose, not DB-filtered — use journal/778 instead), dlc.dlib.indiana.edu (Digital Library of the Commons — governance, off-topic), scholar.google (search tool, not a source). **Discovery tools (added as references, not scans):** semanticscholar.org, core.ac.uk, base-search.net, doaj.org. **Skipped as off-topic for DBMS:** pubmed (biomedical), ssrn (econ/law), plos.org (life sciences), worldwidescience.org (broad federated science).
- (2026-06-28) Engines: added DuckDB (duckdb.org/feed.xml), MotherDuck (motherduck.com/rss.xml), MariaDB Foundation (mariadb.org/feed/) — all real RSS, added to feeds.opml. Also created two cross-index files: `references/taxonomy.md` (by type/role: Publications/Issues/Utilities/News) and `references/source-catalog.md` (by topic; DB as its own category, off-topic disciplines catalogued not scanned, low-quality excluded).

# Source taxonomy (by type / role)

A second, **orthogonal** view of the sources. `source-catalog.md` sorts them by *topic*
(discipline); this file sorts them by *role* — **Publications** (published content) vs **Issues**
(discussion / dev process) vs **Utilities** (search/fact-check tools), with **News** as a
cross-cutting role. The weekly scan list itself lives in `sources.md` / `feeds.opml`; these two
files are lenses over it.

---

# 📚 PUBLICATIONS — published content

### 1. Personal blogs (independent authors)
- Bruce Momjian · Haki Benita · Franck Pachot · Christophe Pettus (thebuild) · Radim Marek (boringsql) · David Wheeler (justatheory) · Oskar Dudycz (event-driven.io) · Markus Winand (modern-sql)
- Andy Pavlo (CMU) · Daniel Abadi (DBMS Musings) · Murat Demirbaş — academic-personal
- Adrian Colyer (The Morning Paper) `[dormant]` · Chinar Aliyev `[dormant]` — paper reviews / archives

### 2. Company / vendor blogs
- **Postgres:** Crunchy Data · pganalyze · EDB · Timescale · Fujitsu Fastware · MS Azure for PG · Postgres.ai · pgMustard · Stormatics · pgEdge
- **Commercial / wider:** DoltHub · DuckDB · MotherDuck · SQL Server (MS) · Oracle Optimizer · Oracle Database Insider · MySQL Server · MariaDB Foundation · Percona · AWS Database Blog
- **Non-English:** Postgres Pro `[ru]` · PingCAP/TiDB `[zh]` · OceanBase `[zh]` · Alibaba Cloud `[zh]` · Dalibo `[fr]` · dbi-services `[fr]` · Cybertec `[de]` · SRA OSS `[ja]`

### 3. Research — papers & preprints
- arXiv cs.DB · Hugging Face Papers · VLDB/PVLDB (proceedings) · SIGMOD (proceedings) · CIDR

### 4. Journals (peer-reviewed periodicals)
- The VLDB Journal (Springer) · ACM SIGMOD Record

### 5. Reference works / books / curated lists
- The Internals of PostgreSQL (interdb.jp) · awesome-database-learning · learn.microsoft.com (SQL Server blog archive) · CITForum `[ru]`

### 6. Aggregators & newsletters
- Planet PostgreSQL · Postgres Weekly · DB Weekly · pganalyze «5mins» · The New Stack · modb.pro `[zh]` · Habr DB hubs `[ru]` · Qiita `[ja]`

### 7. Official announcements / releases
- PostgreSQL News Archive · PostgreSQL git commits (ground truth for fact-check) · PostgreSQL Upcoming Events

### 8. Conferences / CFP trackers
- postgresql.org/events · dev.events · PGConf.dev · PGConf.EU · regional PGDays · ICDE · DEBS · USENIX · WikiCFP · DBWorld

---

# 🗣️ ISSUES — discussion, bugs, dev process

### 1. PostgreSQL development (mailing lists + patches) = "postgres-hackers"
- **Mailing lists:** pgsql-hackers · pgsql-bugs · pgsql-performance · pgsql-general
- **Patches / roadmap:** CommitFest (patches under review)
- **Archive access:** mail-archive.com (read-path) · pghackers.com (AI search over the archive)

### 2. Forums / link aggregators
- Hacker News · Lobsters (databases tag)

### 3. Social networks (Reddit + microblogging)
- r/PostgreSQL · r/databasedevelopment · r/SQL · r/Database · r/dataengineering
- *(microblogging — not yet wired up: Mastodon / Bluesky / X)*

### 4. Q&A
- DBA Stack Exchange · Stack Overflow `[postgresql]/[sql]`

### 5. Chat / messengers
- PostgreSQL Slack `[auth]` · Discord `[auth]` · IRC Libera `[auth]` · Telegram channels

---

# 🔍 UTILITIES — not sources, but search / fact-check tools
- Semantic Scholar · CORE · BASE · DOAJ · Google Scholar

---

# 📰 NEWS — cross-cutting role (a *purpose*, not a separate pile)

### 1. Official project news (releases, CVEs, announcements)
- **PostgreSQL News Archive** — releases, security, extension announcements *(primary)*
- **PostgreSQL git commits** — what actually landed *(ground truth)*
- **postgresql.org/about/events** — "CFP open", conference dates

### 2. Curated news digests / newsletters
- **Postgres Weekly** · **DB Weekly** · **pganalyze "5mins of Postgres"**
- *(this **DBMS Digest** itself belongs here too)*

### 3. DB news media / press
- **The New Stack — Databases** — industry trends/news
- ⏭️ *filtered out as weak-signal / marketing:* InfoWorld · ADTmag · Visual Studio Magazine

### 4. Regional news `[non-EN]`
- **modb.pro** `[zh]` · **Habr DB hubs** `[ru]` · **Qiita** `[ja]` — partly news

---

## Notes on classification edges
- **git commits** and **CommitFest** straddle both axes: commits are a *publication* (a record of
  fact) but used as a verification tool in *issues*; CommitFest is pure *issues* (what's under review).
- **News** is a *role* layered on top of types — e.g. PostgreSQL News Archive is both a
  "publication / official release" and "news"; Postgres/DB Weekly are both "newsletter" and "news".
- This file is the **by-type** axis; `source-catalog.md` is the **by-topic** axis. Both are lenses
  over the same scan list in `sources.md` / `feeds.opml`.

# Source catalog (topic-sorted)

The **maximal** index of every source evaluated for the digest, sorted by topic. This is a
superset of `sources.md` / `feeds.opml`: those two drive the *weekly DBMS scan*, while this file
catalogs everything (including adjacent and off-topic disciplines) for reference and discovery so
nothing is lost.

**The digest only scans the Databases category** below (the `[scan]` items). Everything under the
other disciplines is kept for context / fact-checking, not weekly scanning. Low-quality sources are
deliberately **excluded** (see the bottom of this file for the exclusion log).

**Tags:** `[scan]` in the active DBMS scan · `[ref]` reference / fact-check · `[discovery]` search
tool · `[off-topic]` kept for completeness, not scanned · `[dormant]` inactive · `[paywall]` ·
`[syndication]` republishes others · lang tags `[ru] [zh] [fr] [de] [ja]`.

---

# 🗄️ Databases & DBMS  *(the digest's focus)*

## Dev process — mailing lists & patches *(Issues)*
- pgsql-**hackers** / -**bugs** / -**performance** / -**general** — PostgreSQL mailing lists `[scan]`
- PostgreSQL **CommitFest** — patches under review `[scan]`
- PostgreSQL **git commits** — ground truth for "did X land" `[ref]`
- **mail-archive.com/pgsql-hackers** — archive read-path `[scan]`
- **pghackers.com** — AI search over the hackers archive `[scan]`

## Personal blogs
- Bruce Momjian · Haki Benita · Franck Pachot · Christophe Pettus (thebuild) · Radim Marek (boringsql) · David Wheeler (justatheory) · Oskar Dudycz (event-driven.io) · Markus Winand (modern-sql) `[scan]`
- Andy Pavlo (CMU) · Daniel Abadi (DBMS Musings) · Murat Demirbaş — academic-personal `[scan]`
- Chinar Aliyev — Oracle CBO deep-dives `[ref][dormant]`

## Company / vendor blogs
- **Postgres:** Crunchy Data · pganalyze · EDB · Timescale · Fujitsu Fastware · MS Azure for PG · Postgres.ai · pgMustard · Stormatics · pgEdge `[scan]`
- **Wider / commercial:** DoltHub · DuckDB · MotherDuck · SQL Server (MS) · Oracle Optimizer · Oracle DB Insider · MySQL Server · MariaDB Foundation · Percona · AWS Database Blog `[scan]`
- **learn.microsoft.com — archived SQL Server blogs** — internals archive `[ref]`

## Non-English
- **[ru]** Postgres Pro · Habr hubs (PostgreSQL / SQL / MySQL / NoSQL) · CITForum (DB-theory archive `[ref]`) `[scan]`
- **[zh]** PingCAP/TiDB · OceanBase · Alibaba Cloud (PolarDB/AnalyticDB) · modb.pro `[scan]`
- **[fr]** Dalibo · dbi-services `[scan]`
- **[de]** Cybertec (DE) `[scan]`
- **[ja]** Qiita (PostgreSQL tag) · SRA OSS `[scan]`

## Aggregators · newsletters · news
- Planet PostgreSQL · Postgres Weekly · DB Weekly · pganalyze "5mins of Postgres" `[scan]`
- The New Stack — Databases `[scan]`
- PostgreSQL **News Archive** (releases/CVEs) · PostgreSQL **Upcoming Events** `[scan]`
- **rimzy.net** (Yzmir Ramirez) — MySQL/MongoDB/Percona/HA `[syndication]` (dedupe vs Percona/Planet)

## Research — DB venues, papers, journals
- arXiv cs.DB · Hugging Face Papers (DB-adjacent ML) `[scan]`
- VLDB / PVLDB · SIGMOD · CIDR (proceedings) `[scan]`
- **ACM SIGMOD Record** (quarterly bulletin) · **The VLDB Journal** (Springer, ToC public) `[ref]`
- **The Morning Paper** (Adrian Colyer) — paper reviews `[ref][dormant]`

## Reference / books / curated lists
- **The Internals of PostgreSQL** (interdb.jp) `[ref]`
- **awesome-database-learning** (curated reading list) `[ref]`

## Forums · Q&A · chat *(Issues)*
- Hacker News · Lobsters (databases) `[scan]`
- Reddit: r/PostgreSQL · r/databasedevelopment · r/SQL · r/Database · r/dataengineering `[scan]`
- DBA Stack Exchange · Stack Overflow `[postgresql]/[sql]` `[scan]`
- PostgreSQL Slack · Discord · IRC (Libera) · Telegram channels `[auth]`

## CFP / conference trackers
- dev.events (Postgres) · PGConf.dev · PGConf.EU · regional PGDays · ICDE · DEBS · USENIX · WikiCFP · DBWorld `[scan]`

---

# 🧮 Computer Science *(general — beyond DBMS)*
- **baeldung.com/cs** — CS-concept tutorials (algorithms, data structures); rarely DB `[ref]`
- **datacadamia.com** — computing/data wiki notes `[ref]`
- **thewikihow.com/digest** — aggregates CS group digests (e.g. CMU Database Group); HTTP 403 to plain fetch `[ref][revisit-via-browser]`
- **runebook.dev** — multilingual API-docs mirror (no original content) `[ref][docs-mirror]`
- **packtpub.com** — tutorials/books; mostly promo, occasional author interviews (e.g. Munro on PG parallelism) `[ref][book-promo]`

# 📐 Mathematics
- **MDPI — Mathematics** (open-access journal) `[off-topic][paywall-free]`
- **Springer — Mathematics** (newest-first search) `[off-topic][paywall]`
- **math.stackexchange.com** (Q&A) `[off-topic]`

# 📊 Statistics
- **Springer — Statistics** (newest-first search) `[off-topic][paywall]`

# ⚙️ Engineering / Energy
- **Springer — Engineering / Energy** (newest-first search) `[off-topic][paywall]`

# 🔬 Physics & applied sciences
- **physics.stackexchange.com** (Q&A) `[off-topic]`
- **kitchingroup.cheme.cmu.edu** (John Kitchin — chem-eng / Emacs / scientific computing) `[off-topic]`

# 🧬 Life sciences / Biomedical
- **PubMed / NCBI** (biomedical literature) `[off-topic]`
- **PLOS** (open-access, life sciences) `[off-topic]`

# 💵 Social sciences (economics / law / finance)
- **SSRN** (social-science preprints) `[off-topic]`

# 🏛️ Multidisciplinary journals & publishers
- **Springer** (root) — use specific DB journal (VLDB Journal = journal/778) instead of the firehose `[paywall]`
- **Wiley Online Library** — journal 5192 returned HTTP 402, title unconfirmed `[paywall][unverified]`
- **MDPI** (publisher) — open-access, mixed quality; pick DB-adjacent journals if any

# 🔎 Academic search & discovery engines *(utilities — not scanned)*
- **Semantic Scholar** — AI academic search, strong CS, API `[discovery]`
- **CORE** — largest OA-paper aggregator, API `[discovery]`
- **BASE** — Bielefeld OA search engine `[discovery]`
- **DOAJ** — Directory of Open Access Journals `[discovery]`
- **Google Scholar** — ad-hoc search only `[discovery]`
- **WorldWideScience** — federated science gateway (broad) `[discovery]`
- **Digital Library of the Commons** (dlc.dlib.indiana.edu) — commons/governance research `[discovery][off-topic]`

---

# 🚫 Excluded as low-quality *(not catalogued for use)*
Recorded so they aren't re-submitted/re-evaluated:
- **programmersought.com** — machine-translated SEO scrape of others' posts.
- **independent.academia.edu/IjdmsAircc** (IJDMS / AIRCC) — low-tier journal on a paper-sharing platform.
- **afteracademy.com** — generic, low-signal CS edu content.
- **jianshu.com** — broad blogging platform, no DB curation.
- **cnblogs.com/gaojian** — off-topic (Python basics, not DBMS).

# Sources

The living source list for the weekly DBMS digest. Priority is a rough guide to scan order
(P1 = check every week, P2 = check most weeks, P3 = sample / opportunistic).
When you find a new high-signal source, append it under the right section with a one-line note
and a priority. When a source goes dormant or turns into pure marketing, mark it `[dormant]`
or `[mostly-marketing]` rather than deleting it, so it isn't re-added next week.

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
- **EDB blog** — enterprise Postgres, HA, migrations; filter heavily for marketing. P3. https://www.enterprisedb.com/blog
- **Timescale blog** — time-series / analytics on Postgres; good patterns, watch for product push. P3. https://www.timescale.com/blog
- **Fujitsu (Fastware) Postgres blog** — internals and feature deep-dives. P3. https://www.postgresql.fastware.com/blog
- **Microsoft Azure for PostgreSQL blog** — sometimes solid internals; filter marketing. P3. https://techcommunity.microsoft.com/category/azuredatabases/blog/adforpostgresql
- **Postgres.ai blog** — DBLab, database branching, performance tooling. P3. https://postgres.ai/blog

## PostgreSQL development (primary, highest trust)

- **pgsql-hackers mailing list** — where features are actually designed and argued. Highest signal for "what's coming". P1. https://www.postgresql.org/list/pgsql-hackers/
- **PostgreSQL commitfest** — patches under review; a roadmap of near-term features. P2. https://commitfest.postgresql.org/
- **PostgreSQL git commits** — ground truth for "did X actually land". Use to fact-check claims. P2. https://git.postgresql.org/gitweb/?p=postgresql.git

## Wider DBMS & distributed data

- **Andy Pavlo / CMU DB Group blog** — industry analysis, annual "Databases in <year>" retrospective, seminar series. P1. https://www.cs.cmu.edu/~pavlo/blog/ and https://db.cs.cmu.edu/
- **DBMS Musings (Daniel Abadi)** — isolation/consistency, distributed DB theory made readable. P2. http://dbmsmusings.blogspot.com/
- **Murat Demirbas — Metadata blog** — distributed systems & database papers, paper reviews. P2. https://muratbuffalo.blogspot.com/
- **The New Stack — Databases** — news/trends; mixed, filter for substance. P3. https://thenewstack.io/data/
- **awesome-database-learning** — curated internals reading list; mine for new primary sources. P3. https://github.com/pingcap/awesome-database-learning

## Commercial engines (new techniques & inventions — filter marketing hard)

- **SQL Server — Microsoft engineering blogs & docs** — "What's new" + engine internals; mine for real optimizer/storage/columnstore/Hekaton-style techniques, not feature sheets. P2. https://techcommunity.microsoft.com/category/sql-server/blog/sqlserver
- **Bob Ward / SQL Server team deep-dives** — internals talks and write-ups. P3. https://learn.microsoft.com/en-us/sql/
- **Oracle Optimizer blog** — CBO internals and new optimizer features straight from the team. P2. https://blogs.oracle.com/optimizer/
- **Oracle Database Insider / Maria Colgan** — In-Memory, new-version internals. P3. https://blogs.oracle.com/database/
- **Franck Pachot** — cross-engine internals (Oracle, Postgres, YugabyteDB, MongoDB); excellent technique-level comparisons. P2. https://dev.to/franckpachot
- **MySQL Server Blog / engineering** — InnoDB, optimizer, replication internals. P3. https://dev.mysql.com/blog-archive/
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

## New sources added (log)

_Append discoveries here with date, name, link, and a one-line reason. Example:_
- (2026-06-18) _seed list created._
- (2026-06-18) boringsql.com (Radim Marek) — reproducible Postgres internals deep-dives. https://boringsql.com/
- (2026-06-18) justatheory.com (David Wheeler) — PGXN/extensions + Postgres↔ClickHouse interop. https://justatheory.com/
- (2026-06-18) stormatics.tech — incident-style Postgres ops deep dives. https://stormatics.tech/
- (2026-06-18) thebuild.com (Christophe Pettus) — near-daily GUC-internals series and cross-engine planner deep-dives. P2. https://thebuild.com/blog/
- (2026-06-18) event-driven.io (Oskar Dudycz) — event sourcing / Postgres-as-event-store engineering. P3. https://event-driven.io/
- (2026-06-18) modern-sql.com (Markus Winand) — cross-engine SQL-standard conformance and feature comparisons. P2. https://modern-sql.com/

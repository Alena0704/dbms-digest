# Community sources

The living list of *discussion* sources for the **Community pulse** section — forums, link
aggregators, Q&A sites, and chat/messenger channels where people actually argue about
databases. Distinct from `sources.md` (which lists publishers of articles/releases); this file
lists places where *conversation* happens.

Priority is scan order (P1 = every week, P2 = most weeks, P3 = sample/opportunistic).
Access tier tells you whether it can be scanned without an account:

- `[public]` — readable with web fetch / search, no login. Scan these.
- `[js]` — public but client-rendered; use the in-browser reader, not a plain fetch.
- `[auth]` — needs an account / invite / bot membership. **Not auto-scannable today** — kept
  here so we add it the moment a connector or credential exists. Do not fabricate its content.

## Upkeep rules (run every week)

1. **Rank by engagement.** A thread earns a spot by how much real discussion it drew
   (HN points + comments, Reddit upvotes + comments, SE votes/answers), not by mere existence.
2. **Dedupe against the rest of the digest.** If a thread is just people reacting to an article
   already listed above, fold it in / skip it. The Community pulse is for discussion that is
   itself the story (debates, war stories, "wait, does Postgres really do X?").
3. **Discover.** Each run, spend a little effort finding *new* active DB communities —
   a fresh subreddit, a Discourse forum, a public Telegram channel, a Matrix room, a Discord
   that opened public logs. Add keepers below with date, access tier, and a one-line reason.
4. **Prune.** If a listed source shows no database activity in ~3 months, is gone, or has turned
   into pure self-promotion, **move it to the Retired log** at the bottom (with date + reason).
   That removes it from the weekly scan but records it so it isn't blindly re-added next week.

---

## Forums & link aggregators

- **Hacker News** — search the week's DB threads and rank by points/comments; query `postgres`,
  `postgresql`, `database`, `sql`, `duckdb`, `clickhouse`, `sqlite`, `mysql`. Best signal-to-noise
  for cross-engine debate. `[public]` (Algolia API: hn.algolia.com). P1.
- **Lobsters — databases tag** — smaller, higher-signal than HN; good for systems/internals.
  `[public]` https://lobste.rs/t/databases . P2.
- **r/PostgreSQL** — the main Postgres subreddit; sort Top / This Week. `[js]`
  https://www.reddit.com/r/PostgreSQL/top/?t=week . P1.
- **r/databasedevelopment** — DB *internals* community (storage engines, query processing);
  exactly the reader's wheelhouse. `[js]` https://www.reddit.com/r/databasedevelopment/ . P1.
- **r/SQL** — broader SQL Q&A and discussion; filter heavily. `[js]`
  https://www.reddit.com/r/SQL/top/?t=week . P2.
- **r/Database** — general DB talk; smaller, noisier. `[js]`
  https://www.reddit.com/r/Database/top/?t=week . P3.
- **r/dataengineering** — pipelines/warehouses; lots of vendor noise, occasional gold. `[js]`
  https://www.reddit.com/r/dataengineering/top/?t=week . P3.

## Q&A

- **DBA Stack Exchange** — "hot this week" surfaces real operational puzzles and surprising
  answers. `[public]` https://dba.stackexchange.com/?tab=week . P2.
- **Stack Overflow — [postgresql] / [sql]** — high volume, mostly routine; sample only for a
  question that blew up or got an authoritative answer. `[public]`
  https://stackoverflow.com/questions/tagged/postgresql?tab=Week . P3.

## Chat & messengers

- **PostgreSQL community Slack** — postgresteam.slack.com (join via https://postgres-slack.org).
  High-signal real-time talk. `[auth]` — needs invite; not auto-scannable yet. P-.
- **PostgreSQL Discord** — public server but reading history needs membership/bot. `[auth]`. P-.
- **#postgresql on Libera.Chat (IRC)** — public channel, but no reliable public web archive.
  `[auth]` (effectively). P-.
- **Public Telegram channels** — readable without login via the web preview
  `https://t.me/s/<channel>`. None pinned yet — **discover and add** the ones worth following
  (English and Russian-language Postgres/DBMS channels). `[public]` once a channel is named. P2.

---

## Discovery log

_Append new community sources here: date, name, link, access tier, one-line reason._
- (2026-06-20) _seed list created._

## Retired (removed from weekly scan)

_When a source goes dead/dormant/promotional, move it here with date + reason so it isn't
re-added by mistake._
- _(none yet)_

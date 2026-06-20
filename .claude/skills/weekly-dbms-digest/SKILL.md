---
name: weekly-dbms-digest
description: Build a weekly, ad-free digest of PostgreSQL and broader DBMS news, research, and cutting-edge tech — including new techniques and inventions in commercial engines (SQL Server, Oracle, MySQL, etc.) and real-world migration experience reports. Use this skill whenever the user asks for the "weekly digest", "Postgres digest", "DBMS digest", "database news roundup", "what happened in databases this week", or when a scheduled task asks to generate the weekly database digest. The skill curates high-signal sources, finds items published in the last 7 days, ruthlessly filters out advertising / vendor promotion / marketing fluff, fact-checks claims, and emits a terse headline + one-line list of links. It also discovers and records new emerging sources each run so the source list stays fresh.
---

# Weekly DBMS Digest

Produce a short, high-signal weekly digest of what actually happened in the PostgreSQL and wider database world: new technologies, real engineering, cutting-edge inventions, and research. This explicitly includes new techniques and inventions in **commercial engines** (SQL Server, Oracle, MySQL, DB2, etc.) and **real-world migration experience** reports — the reader cares about what other databases are doing and what actually happens when people move data between them. The reader is a Postgres hacker who is allergic to marketing. The single most important job of this skill is to **separate signal from sales**: surface genuine technical/research content and discard (or clearly flag) advertisement, company promotion, and marketing material.

The output is deliberately terse: each item is a **headline + one line** with a link. The reader wants to scan 15–30 items in two minutes and click into the 3–4 that matter.

## Workflow

Follow these steps in order. Don't skip the filtering and fact-check steps — they are the whole point.

### 1. Establish the time window

The digest covers the **last 7 days** by default (or the span since the previous digest if the user gives one). Compute the date range with `date` so you don't rely on a guessed "today". Items published outside the window are excluded, even if interesting — note them only if genuinely seminal.

### 2. Gather candidate items from known sources

Read `references/sources.md` for the curated source list, grouped into Postgres, broad DBMS, research venues, and aggregators/newsletters. Work through the high-priority sources first. Prefer aggregators (Planet PostgreSQL, DB Weekly) to fan out quickly, then go direct to primary blogs for anything promising.

Use web search and page fetches to collect: title, URL, author/source, publish date, and enough of the body to judge it. Cast a wide net here — filtering happens next.

### 3. Scan PostgreSQL mailing lists

Scan the four key lists for the current time window. Use the PostgreSQL list archives at `https://www.postgresql.org/list/<listname>/` (monthly view) or web-search `site:postgresql.org/message-id` with topic keywords to pull specific threads.

**Lists to scan (in priority order):**
- `pgsql-hackers` — new feature proposals, patch reviews, design debates, committer decisions
- `pgsql-bugs` — confirmed bugs and surprising regressions; ignore "user error" threads
- `pgsql-performance` — unexpected slowdowns, benchmark surprises, planner misbehaviour reports
- `pgsql-general` — only surface items where a core developer or committer gave a notable/surprising answer; skip routine user questions

**What qualifies** (be selective — list traffic is high; signal is rare):

*New threads worth surfacing:*
- A new feature or design proposal with a concrete patch or detailed spec
- A confirmed bug or regression with a reproducible test case or bisected commit
- A benchmark result or performance finding that is surprising relative to prior behaviour
- A design debate where the outcome (accept / reject / defer) is itself informative
- A security or data-loss risk being actively discussed

*Changes in ongoing threads worth surfacing:*
- A thread that was stalled or controversial and just reached a resolution (committed, rejected, redesigned)
- A significant objection raised against a previously-accepted approach
- New data (benchmark, counter-example, real-world report) that materially shifts the discussion
- A committer expressing a strong opinion that narrows or redirects the design space

**What to skip:**
- "How do I do X?" threads without a core-developer surprise in the answer
- Patch submissions still in early review with no substantive feedback yet
- Threading noise: replies that just say "+1" or "thanks"
- Build/packaging questions unless a portability bug is confirmed

**How to search:** For each list, search for messages posted in the current week using queries like `pgsql-hackers <topic keyword> site:postgresql.org/message-id` or fetch the monthly archive index. For performance and bugs lists, also try `pgsql-performance regression 2026` or `pgsql-bugs <version>`. Aim to scan at least the subject lines of the top 20–30 threads per list before choosing items.

**Format for mailing list items** (goes in the `## PostgreSQL mailing lists` section):
```
- **[hackers] [<Thread subject>](archive URL)** — <one line: what was proposed/found/decided and why it matters>. *(<proposer/committer>)* `[patch posted]`
- **[bugs] [<Thread subject>](archive URL)** — <one line: confirmed bug / regression / data-loss risk>. *(<reporter>)* `[open]`
```
Tag with the list name in brackets and make the **thread subject the link** — to the thread root in the archive, not a specific reply (unless a specific reply is the event). Add the key person (proposer / committer / reporter) in italics after the line, e.g. `*(Jeff Davis · pgsql-hackers)*`. Append `[committed]`, `[rejected]`, `[patch posted]`, `[needs review]`, or `[open]` to show where things stand.

### 4. Discover emerging sources (self-update)

Each run, spend a little effort looking for **new, high-quality sources** that aren't yet in `references/sources.md`: a new independent engineering blog, a fresh research group page, a newly active newsletter, a conference that just posted proceedings. Good signals are: cited by sources you already trust, written by known contributors, deep technical content with no sales pitch.

When you find a keeper, **append it to `references/sources.md`** under the right section with a one-line note on why it's worth watching. This is how the skill stays current instead of going stale. Conversely, if a listed source has gone dormant or turned into pure marketing, mark it accordingly.

### 5. Filter out marketing, ads, and promotion

This is the core value of the digest. **Exclude** an item (or flag it clearly if it's borderline but still has real content) when it shows the hallmarks of marketing rather than engineering:

- It's primarily announcing a product, pricing, funding round, partnership, award, or "we're now GA" with little technical substance.
- It's a vendor case study whose real purpose is the logo and the CTA, not the method.
- Superlatives without numbers: "blazing-fast", "next-gen", "revolutionary", "game-changing", "enterprise-grade" with nothing measured.
- It ends in a demo booking, free-trial, or "talk to sales" call to action and the body was just a runway to it.
- Reposted press release / sponsored content / listicle SEO bait ("Top 15 databases for 2026").

**Keep** content that teaches or proves something: benchmarks with methodology, internals deep-dives, postmortems, release notes that explain *what changed and why*, research papers, protocol/design discussions, reproducible experiments — even when published on a vendor's blog. A vendor engineering blog post can be excellent; judge the substance, not the domain. When in doubt, ask: "If I strip the company name, is there still something I learned?" If no, cut it.

**Feature-explainer rule (authority gate).** A lot of posts just describe a new or existing feature without adding a new use case, a problem found in the wild, a benchmark, or a non-obvious gotcha. These "here's how feature X works" walkthroughs are only worth including when written by someone with first-hand authority over that feature — its **author, committer, or reviewer** (for Postgres, check the commit / CommitFest / release-note credits; for other engines, the engineer who built or shipped it). If a generic feature explainer is written by someone *without* that direct involvement, skip it — it's usually a rehash. The exception is the moment a feature first ships (a release/beta announcement), which is news regardless of author. When you do include an authority-written feature post, you may note the author's role, e.g. `[by committer]`.

**Commercial-engine techniques.** Actively look for genuinely new techniques and inventions in SQL Server, Oracle, MySQL, DB2, and similar — new optimizer/storage/replication capabilities, internals write-ups, and engineering deep-dives. Apply the same anti-marketing filter: a real technique or measured result, not a "what's new in version N" sales sheet.

**Release posts get a changes summary.** When an item is the release of an extension or utility (e.g. "pg_kpart 1.0", "powa-archivist 5.1.2", "pgBackRest 2.x"), don't just say "new release" — read the changelog/release notes and summarise *what actually changed*: the headline new features, notable fixes, breaking changes, and the minimum/target server version. This is the one place to relax the strict one-line limit — a release item may use a short sub-bullet list of the key changes when that's clearer. Skip pure version-bump posts with no meaningful changes, and still drop release posts whose "changes" are entirely marketing.

**Migration experience.** Actively look for real-world migration experience reports — moving to/from Postgres, Oracle→Postgres, MySQL→Postgres, cross-cloud, version upgrades at scale — where the author shares what actually happened (pitfalls, downtime, data discrepancies, tooling, rollback). These are high-value; prioritise them. Generic "why you should migrate to our product" posts are marketing — cut them.

### 6. Fact-check before including

For each surviving item, do a quick sanity pass: does the headline claim match the body? Are benchmark claims accompanied by setup details (hardware, dataset, versions)? Is a "Postgres now does X" claim actually in a release/commit, or just speculation? Cross-check surprising claims against a second source (commit, mailing-list thread, the actual paper). If a claim can't be substantiated, either drop the item or append a short `[unverified]` note so the reader knows.

### 7. Write the digest

Use the exact format below. Keep each line to roughly one sentence — the value is in being scannable. Order items by importance (most significant first), lightly grouped by theme. Aim for ~10–25 items; quality over quantity. If a slow week yields little, a short honest digest beats padding.

## Output format

```
# DBMS Weekly — <YYYY-MM-DD> (week of <start>–<end>)

## PostgreSQL
- **[<Headline>](URL)** — <one-line why-it-matters>. *(<Author> · <source>)*
- ...

## PostgreSQL mailing lists
- **[hackers] [<Thread subject>](archive URL)** — <one line: what was proposed/found/decided>. *(<proposer>)* `[patch posted]`
- **[bugs] [<Thread subject>](archive URL)** — <one line: confirmed bug or regression>. *(<reporter>)* `[open]`
- ...

## Wider DBMS & distributed data
- **[<Headline>](URL)** — <one line>. *(<Author> · <source>)*
- ...

## Commercial engines (SQL Server, Oracle, MySQL, …)
- **[<Headline>](URL)** — <one line on the new technique/invention>. *(<Author> · <source>)*
- ...

## Migration experience
- **[<Headline>](URL)** — <one line on what actually happened>. *(<Author> · <source>)*
- ...

## Research & cutting edge
- **[<Headline>](URL)** — <one line>. *(<authors / venue>)* _[paper]_
- ...

## New sources added this week
- **[<source name>](URL)** — <why it's worth following>. *(<author>)*

---

_<N> items · sources scanned: <count> · filtered out as marketing/ads: <count>_
```

Notes on the format:
- **The headline is the link** (`**[Headline](URL)**`) — one big tap target, ideal on a phone; do not add a trailing `[link]`. The one-liner says *why a Postgres hacker should care*, not just what it is.
- **End each item with the author/source in italics**, e.g. `*(Christophe Pettus · thebuild.com)*`. Include the author's name when it isn't already in the one-liner; otherwise just the source/site (or venue, for papers). On a phone this lets the reader triage before tapping.
- Append `[paper]`, `[unverified]`, `[by committer]`, or `[vendor blog — substantive]` tags only when useful.
- **Release items** (extension/utility releases) may break the one-line rule: give a headline line plus an optional short indented sub-list of the key changes (new features, notable fixes, breaking changes, target server version). Example:
  ```
  - **[pg_kpart 1.0](URL)** — new index-time guard against full-partition scans. *(<author> · <source>)*
      - rejects queries that scan all partitions without the partition key
      - PostgreSQL 18+
  ```
- **Skip empty sections silently.** Omit any section that has no items — do NOT write "nothing this week", "no items found", or an apology/explanation. A missing section just means nothing qualified; the reader infers that. Never add filler narration about gaps.
- If delivering to Telegram or another plain-text channel later, the same content works; just drop the Markdown headers to bullet groups if the target doesn't render Markdown.

## Example items

**Good (keep):**
`- **[Skip scan lands in Postgres 18](URL)** — btree now skips leading index columns, killing a class of "add a redundant index" workarounds; commit shows up to 20x on low-cardinality prefixes. *(pganalyze.com)*`

`- **[hackers] [Rethink hash join memory accounting](URL)** — Melanie Plageman proposes replacing the current executor-side batch-spill heuristic with a planner-visible cost model; thread has substantive back-and-forth on the right abstraction boundary. *(Melanie Plageman · pgsql-hackers)* [patch posted]`

`- **[bugs] [Logical replication silently drops rows on publisher restart under load](URL)** — confirmed regression in 17.2, bisected to commit abc1234; workaround posted, fix in progress. *(pgsql-hackers)* [open]`

**Bad (filter out):**
`- "Acme DB raises $40M Series B to revolutionize the cloud-native AI-ready database" — funding announcement, no technical content. (excluded)`

`- **[general] How do I speed up my query?** — routine user question with no surprising answer. (excluded)`

## Keeping the skill healthy

The source list is the skill's memory. Treat `references/sources.md` as a living file: add what proves valuable, demote what turns into a billboard. Over a few months this should converge on a personal, high-trust set of sources tuned to what the reader actually finds worth reading.

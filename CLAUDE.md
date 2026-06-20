# dbms-digest — project instructions

This repo holds a personal **weekly DBMS digest**. Each digest is one Markdown file in
`digests/`, and `README.md` keeps a dated index linking to every digest.

## Run this routine on every open

Whenever you open this project (in Cowork or Claude Code), run the following routine
**automatically, before anything else**, then report what you did:

1. **Take stock.** List `digests/` and read the index links in `README.md`. Each digest
   file is named `digests/YYYY-MM-DD.md`, dated to the **Monday** that starts the week it
   covers.

2. **Find the missing weeks.** The cadence is **weekly, Monday → Sunday**. Compute, with
   `date`, the **4 most recent *completed* weeks** (a week is complete once its Sunday has
   passed). Any of those 4 Mondays without a matching `digests/<Monday>.md` file is a gap to
   fill. Do **not** generate the current in-progress week.

3. **Generate the absent digests.** For each missing week, use the **`weekly-dbms-digest`**
   skill (`.claude/skills/weekly-dbms-digest/SKILL.md`) to build that week's digest over the
   exact Monday→Sunday window. Follow the skill in full — gather, scan the mailing lists,
   scan the community sources for the **Community pulse**, discover sources, filter out
   marketing, fact-check — and write the result to `digests/<Monday>.md`. Generate oldest-first.

4. **Update the index.** Add a link to each new digest in the `## Digests` section of
   `README.md`, newest first: `- [YYYY-MM-DD — week of …](digests/YYYY-MM-DD.md)`.

5. **Keep sources fresh.** The skill may edit its source lists —
   `.claude/skills/weekly-dbms-digest/references/sources.md` (publishers) and
   `references/community-sources.md` (forums/chats/channels: new ones discovered, dead ones
   retired). Include those edits in the commit.

6. **Rebuild the RSS feed.** Whenever any digest was added or changed, run
   `python3 scripts/build_feed.py` to regenerate `docs/feed.xml` and `docs/index.html` from the
   digests. The feed is what people read on their phones; keep it in sync.

7. **Commit and push.** Stage the new digest files, the README change, any sources update, and
   the regenerated `docs/` files, and commit with a message like
   `digest: add weeks YYYY-MM-DD … (auto)`. One commit per run is fine. Then `git push` to
   `origin` so the feed and GitHub Pages site update. If the push fails (no credentials, no
   network), keep the local commit and report that the push needs to be done manually.

If there are no gaps, say so and make no commit.

## Conventions

- Digest filename = the **Monday** date of the covered week (`digests/2026-06-08.md`).
- A digest's window is that Monday 00:00 through the following Sunday 23:59.
- Keep digests terse and ad-free, exactly as the skill specifies. Quality over padding —
  a short honest week beats filler.
- The published feed lives at `docs/feed.xml` (RSS) with a landing page at `docs/index.html`,
  served by GitHub Pages from `main` → `/docs`. The generator is `scripts/build_feed.py`.

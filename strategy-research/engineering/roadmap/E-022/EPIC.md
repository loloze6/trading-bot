# E-022 — Automated "what's happening" digest, every 2 days

**State:** in-progress
**Owner:** Jérémy (joint with Dorian — it reports on his work too)
**Updated:** 2026-08-13

## Why

Both people currently piece status together by hand from git, Slack, and
Notion — Dorian's own "Mac fork wrap" posts are a manual version of exactly
this. A lightweight automated digest, posted every 2 days, removes that
manual step using only what's already recorded elsewhere (git commits/PRs,
`EPICS.md`, the Notion Bugs & Tasks board) — no new state store, consistent
with `PROCESS.md`'s existing "Notion is a notification surface" principle,
just applied here with Slack as the delivery surface instead of a database.

Deliberately scoped small at Jérémy's explicit request ("simple for now,
iterate later") — see Log for what's cut from v1 on purpose.

## Done when

A Slack message posts to `#tradingbot` every 2 days, containing:

1. Latest completions (cap 3 — whatever mattered most, not a full changelog)
2. To-do / next-step actions (from `EPICS.md`'s Next-step column + open
   Notion Bugs & Tasks cards)
3. Ongoing work per collaborator (commits/PRs opened by each author in the
   period — pulled from git/GitHub, not self-reported)
4. Open improvements (open epics, from `EPICS.md`)
5. Open bugs (open Notion Bugs & Tasks cards)
6. One shared northstar line, plus an optional one-line "current focus" tag
   per collaborator underneath it (not two separate northstars)

Verified by: two consecutive real firings that each produce a correct,
non-empty digest matching the actual repo/board state at that time.

## Stories

- [x] S1 — Write the digest logic: what to query for each of the 6
      sections above, and the format (bold section headers + bullets,
      matching Dorian's existing wrap-up style — no markdown tables, reads
      badly in Slack/mobile).
- [x] S2 — Wire it as a scheduled routine, firing every 2 days, posting to
      `#tradingbot`.
- [ ] S3 — Run it for 1-2 cycles, sanity-check the output against reality,
      adjust based on what's actually useful vs. noise before treating the
      format as settled.

## Log

- 2026-08-13 — `new`. Follows directly from a "who does what" communication
  gap discussed with Jérémy + agent. Cadence set to every 2 days (weekly
  judged too slow). Scoped deliberately minimal — cut from v1 on purpose,
  to revisit later: a drift/staleness check between git and Notion (the
  exact bug caught 3x this week — see E-021), an "aging" flag for
  neglected high-priority items, and switching the open-bugs source from
  Notion to GitHub Issues once E-021 resolves.
- 2026-08-13 — `new` → `in-progress`. S1+S2 dispatched together: digest
  logic written directly into the schedule's prompt (no separate code —
  v1 is agent-generated per firing, not a script) and wired as trigger
  `trig_01CQM7EHZbCriuViY8bYh1bP`, cron `0 8 */2 * *` (UTC), self-bound to
  the existing session — same connector-access constraint as E-021's
  interim sync routine (this org can't grant Notion/Slack access to a
  freshly spawned session via a trigger). Fired once manually same-day to
  produce a first real output for the S3 sanity check.

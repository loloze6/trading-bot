# E-022 — Automated "what's happening" digest, every 2 days

**State:** done
**Owner:** Jérémy (joint with Dorian — it reports on his work too)
**Updated:** 2026-08-14

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
- [x] S3 — Run it for 1-2 cycles, sanity-check the output against reality,
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
- 2026-08-13 — S3, first real run. Posted to #tradingbot
  (p1786650635663579). Sections 1-3, 5, 6 (completions, next actions,
  per-collaborator activity, open bugs, northstar) read correctly against
  real git/GitHub/Notion data. Section 4 (open improvements) listed all 19
  active epics and was too long for a scan-in-a-minute digest — flagged in
  the post itself. Candidate v2 fix: show only in-progress + new-this-week
  by default, cite `EPICS.md` for the rest instead of repeating it.
- 2026-08-13 — Cost/architecture concern raised: the self-bound trigger
  means every firing re-processes this session's entire (growing) history,
  not just its own ~6-8 tool calls — cost per firing rises over time, and
  the harness's auto-compaction (which prevents a hard failure at the
  context limit) trades that off against detail loss on older decisions.
  Checked whether a genuinely stateless fresh session could work instead:
  `ListConnectors` confirms Notion and Slack ARE real, connected,
  account-level connectors (`connected: true`, `enabledInChat: true`) —
  not an environment-only quirk. The actual blocker is narrower: this
  session's own `create_trigger` calls cannot attach connector grants to a
  freshly-spawned session for this org (`connectors` parameter itself
  disabled — "not available for this organization"), most likely a
  deliberate gate on agent-initiated recurring connector access rather
  than a statement that it's impossible. Plan: Jérémy to try creating the
  equivalent routine directly via the claude.ai Routines UI (human-driven
  connector grant may not be subject to the same gate). If that works,
  migrate E-022 off the self-bound session onto a fresh-session routine —
  fixes the cost/detail-loss concern structurally. If it also blocks
  connectors, fall back to (a) periodically re-binding this routine to a
  freshly reset session, or (b) replacing the mechanical
  query-format-post steps with a plain script against the Notion/GitHub/
  Slack APIs directly — no LLM/session involved at all for that part,
  since the job is stateless by nature. Not yet actioned either way.
- 2026-08-14 — Resolved, and `done`. Jérémy created the equivalent routine
  directly via the claude.ai Routines UI (`trig_01XUckqVaSTdJ4rjPABhKZWv`,
  "Updates on engineering progress", same `0 8 */2 * *` schedule, fired
  manually to test). Confirmed via `list_triggers` that this is a
  genuinely different, better architecture than the session-bound
  workaround: its `job_config` shows no `persist_session` and its own
  dedicated `mcp_connections` (Notion, Slack, plus a `visualize` connector
  Jérémy also has) — a fresh session per firing, own git branch each time,
  zero accumulated history. This fully resolves the prior cost/detail-loss
  concern; the self-bound fallback (`trig_01CQM7EHZbCriuViY8bYh1bP`) is
  now redundant and was DELETED (it would otherwise have double-posted
  alongside the new routine on 2026-08-15, same time slot).
  Done-when evidence — two real firings, each correct and non-empty:
  1. 2026-08-13 21:50 CEST, self-bound trigger (p1786650635663579).
  2. 2026-08-14 10:33 CEST, new claude.ai-UI routine (p1786696390584949).
  Both correctly reflected real git/GitHub/Notion state and, per the
  plan, self-flagged rather than guessed on 3 real sourcing gaps in run 2:
  (a) E-020/E-021/E-022 live only on branch `claude/test-5yopd3`, so
  `EPICS.md` as read from `master` omits them — landing that branch fixes
  this; (b) Notion's Bugs & Tasks schema has no last-edited timestamp, so
  "Done in the last 2 days" is inferred from GitHub merge dates, not
  queried directly; (c) 15 of 66 open cards are untriaged (no status set).
  None of these block Done — they're the exact kind of finding S3 exists
  to catch. Deferred to a later pass (small edits to the trigger prompt,
  not a new epic): trim the *Open improvements* section (still lists all
  16-19 epics) to in-progress + new-this-week; and reconsider the
  Northstar line's "unless a later message in this session says it
  changed" instruction, which assumed session continuity that no longer
  exists now that the real routine is stateless per firing.

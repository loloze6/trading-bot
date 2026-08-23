# E-031 — Queue return edge: the loop must be able to start a new line of inquiry

**State:** in-progress (S1 dispatched 2026-08-23)
**Owner:** Jeremy
**Updated:** 2026-08-23

## Why

The research loop has been idle since 2026-07-19. It did not crash and nobody
stopped it — it ran out of work and has no way to give itself more.

Opened from a `research-system-evolution` review (2026-08-23), on four
measurements against primary artifacts:

- **The queue has zero schedulable entries.** `config/campaign_queue.yaml`
  holds 4 entries: 3 `done`, 1 `blocked_on_daily_bar_ingest`. `_select_entry`
  (`run_campaign.py:148`) selects on exact equality with `ready`/`in_progress`.
  Nothing matches.
- **No code path can append one.** `register_hypothesis()` is the only
  queue-append function. Its callers across the whole repo: one CLI argparse
  dispatch (`run_campaign.py:2119`) and four tests. Zero in-pipeline callers.
  It has been invoked **once in the system's entire life** — 2026-07-18, by
  hand (1 REGISTER line in `campaign_log.md`, whole history).
- **The stage graph has no return edge.** `verdict_interpreter` and
  `campaign_review` both declare `next: []` in `workflow/stages.yaml`.
- **Exhaustion is a clean exit, not an error.** `process_once()` logs one line
  and returns `False`. The last line the machine ever wrote, verbatim:
  `2026-07-19T12:29:11Z Queue exhausted — no ready or in_progress entries remain.`

Context for scale: **35 days idle, 455 commits landed in the same window**
(`git log --since=2026-07-19 | wc -l`). The machine that builds the machine ran
flat out; the machine that finds strategies was off the whole time.

The loop *can* continue a lineage — 19 of 36 completions are
`completed_refined`, 11 `completed_reframed`, and `P4_ts_trend` carries three
run IDs under one entry. What it cannot do is open a **new** one. Every lineage
terminates; when the last one does, the machine stops and stays stopped.

### E-030's instrument is blind to this state

All four `_write_loop_health()` call sites sit at line 1801 and beyond; the
queue-exhausted `return False` is at line 1765. The loop-health block never
runs on the one condition that has actually stopped the loop. This is not a
flaw in E-030 (scoped to halts) — it is evidence that **halted** and **idle**
are different states and only one is instrumented. `loop_health.yaml` does not
exist on disk, because no `process_once()` step has run since it was built.

## Done when

1. A terminal stage can route to a new queue entry instead of to `next: []`.
   The routing decision and its seed source are recorded, not implicit.
2. A schedulability block is written **before** the exhaustion return on every
   `process_once()` step: ready / in_progress / blocked counts, days since last
   completion, per-blocked-entry dwell time and blocker string. Consumed by
   `run_campaign.py`'s own refill-vs-escalate decision, not only read by a
   human (F3/F6).
3. Every auto-minted queue entry gets a trial row. Autonomous generation that
   does not count itself silently inflates N for every future deflated-Sharpe
   claim — the same failure E-025 exists to prevent between two human writers,
   with a machine as the second writer.
4. Off by default behind a flag, with a test proving byte-identical behaviour
   when the flag is off.
5. Fast suites green both repos; slow suite green or an output change declared
   with a before/after artifact diff.

## Stories

- [x] S1 — **Characterize and STOP.** Which seed sources are legitimate for a
      refill (`failed_families`, `feed_wishlist`, KB reactivation clauses,
      `refinement_planner`'s deferred branches), what each can actually supply
      today, and what the routing policy should be. No code. The graph edge is
      trivial; the policy is the work.
- [ ] S2 — The schedulability block, written before the exhaustion return.
      Standalone value: it makes "the loop is idle" visible even before refill
      exists.
- [ ] S3 — The return edge itself, plus trial accounting on auto-minted
      entries, off by default with the bit-identity test.

## Relationship to other epics

- **E-030** (halt recovery) — done 2026-08-23; this is the successor the
  operator sequenced on 2026-08-21 (halt recovery → queue self-refill →
  E-029 → E-027). E-030 made the loop survive a transient failure; this makes
  it survive its own success.
- **E-032** (proactive idea generation) — the quality half. E-031 is the
  plumbing that lets an idea reach the queue; E-032 decides whether the idea is
  worth having. **Building E-031 alone yields a machine that re-queues
  neighbours of dead families, faster than before.** Both are needed.
- **E-025** (dual-writer ledger) — Done-when #3 must be consistent with
  whatever E-025 settles on trial-ID allocation. A machine writer is a third
  writer.

## Success signal (pre-registered, per the skill's A8)

Within 30 days of shipping: at least one queue entry appears with
`source != operator_ratified` and reaches a terminal `completed_*` state
without a human authoring its brief. Check by diffing `campaign_queue.yaml`
and counting REGISTER lines in `campaign_log.md` (baseline: 1, whole history).

## Log

- 2026-08-23 — `new`. Opened from a `research-system-evolution` review, on the
  four measurements above. Split from a single proposal into E-031 (plumbing)
  and E-032 (idea quality) at the operator's direction — Part A is a day's
  work and gets the loop moving; Part B carries the real design risk and
  deserves its own characterize-and-stop.
- 2026-08-23 — S1 done. Full report:
  `artifacts/s1_refill_sources.md`; measurements reproducible via
  `artifacts/s1_measure_refill_sources.py` (read-only). Headline findings:
  (1) of every candidate seed source examined, exactly one has a real, open,
  unblocked candidate today — the 4h-timeframe branch of the
  `funding_rate_continuous_mean_reversion_expanded_auto` KB reactivation
  clause (its daily sibling branch already ran and was killed as
  `FUNDING_MR_DAILY_RETEST`/`run_059`; the 4h branch is explicitly recorded
  as "DEFERRED and untouched"). (2) A second wishlist-style gate exists
  beyond the ones named in the story brief — `config/detector_wishlist.yaml`,
  3 machine-checkable regime-detector candidates — but its single-authority
  write function (`evaluate_and_persist_wishlist_predicate`) has zero callers
  anywhere in the repo, so its `not_triggered` status is stale by
  construction (pinned to 2026-07-10, ~15 KB findings postdate it). Same
  failure shape as `register_hypothesis`: a correct write path nobody calls.
  (3) `QUEUE_ENTRY_SCHEMA`'s `source` field is a closed 3-value enum
  (`agent`/`operator_ratified`/`user_delivered`) and the schema is
  deny-by-default — **no queue entry can legally declare "a machine minted
  this" today**, on either axis (no fitting enum value, no room for a new
  field without a schema change). (4) Confirmed by direct read: none of the
  4 `_write_loop_health()` call sites (1801/1932/1944/1968) sit before the
  `entry is None` exhaustion return at 1764-1766 — the loop-health block
  genuinely never runs on that path. (5) `campaign_state.yaml`'s
  `instruments_tried`/`timeframes_tried` are stale (never updated after
  XS_momentum's 19-pair universe ratification or the P4 daily-bar landing) —
  flagged so S3 doesn't trust them uncorrected. Recommended policy for S3:
  auto-mint candidates into `status: paused:pending_operator_ratification`
  (fits the existing status regex, no schema change needed there), never
  straight to `ready`; treat zero admissible candidates as a legitimate,
  instrumented terminal state rather than something to route around; add a
  third disjoint run-ID prefix (e.g. `run_a_NNN`) alongside E-025's
  `run_NNN`/`run_d_NNN` so trial accounting — already correct and
  per-run, confirmed by reading `_record_prescreen_trial`/
  `_record_backtest_trial` — never collides across writers. Full build list
  for S3 (schema change, refill function, flag, tests) is itemized in the
  artifact so S3 is a dispatch, not a design session.

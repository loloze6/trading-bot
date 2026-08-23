# E-030 — Halt recovery + a loop-health instrument

**State:** done (2026-08-23 — S2b explicitly parked, not blocking; see Log)
**Owner:** Jeremy
**Updated:** 2026-08-23

## Why

Split out of **E-009** (pipeline harmonization) S3/S4 — those two stories were
filed on 2026-08-03 with their own Done-when admitting "or this sub-item is
re-scoped once S3/S4 below determines the true gap." This epic supplies that
determination and gives the two stories a home sized to their actual priority,
which turned out to be the highest-leverage gap on the whole board.

Opened from a `research-system-evolution` review (2026-08-21). Two
measurements, both against primary records — the campaign's own
`campaign_log.md` (append-only, written by `run_campaign.py`) and each run's
own `pipeline_state.yaml` — converged on the same constraint from different
angles.

### Measured: halt cost (`artifacts/measure_halt_cost.py` / `measured_halt_cost.txt`)

Across `campaign_log.md`'s entire life (2026-07-06 → 2026-07-19, 310.5 h):

```
halts                    : 14
total recorded downtime  : 127.0 h  (5.3 days)
median halt downtime     : 1.98 h
share of span halted     : 40.9%
```

Cause breakdown: 10 of 14 halts (106.6 of 127.0 h, 84%) were plumbing —
`unhandled_exception` (6), `component_execution_error` (3), `component_gap`
(1) — not research-integrity pauses. Two of those 14 halts (21.9 h) are
**already fixed**: a targeted single-retry now exists in
`run_phase1_research.py` for one specific SDK misclassification
(`_SDK_ERROR_RESULT_SUCCESS_MSG`). Still-live plumbing downtime: **84.7 h,
67% of total.** That existing retry is itself evidence for this epic — the
system already has ad-hoc, one-defect-at-a-time recovery; what it lacks is a
general policy.

### Measured: throughput collapse (`artifacts/measure_throughput_eras.py` /
`measured_throughput_eras.txt`), and a correction to a claim made earlier in
this same review

An earlier pass of this review read only `campaign_log.md` and concluded the
workflow had completed "4 runs in its entire life" — wrong, caught by the
operator ("no the research workflow has run 50+ runs.. look locally"), because
`campaign_log.md` only covers the `run_campaign.py` queue-driver era
(run_053 onward); runs 001–052 were driven directly and never wrote to that
log. Re-measured from each run's own `pipeline_state.yaml` (58 state files
across 59 run dirs; 46 with parseable audit timestamps) instead:
**36 runs reached a terminal `completed_*` state.**

Corrected throughput, by era:

```
BEFORE run_campaign.py (pre 2026-07-06): 30 completions / 9.9 days  = 3.02/day
AFTER  run_campaign.py (2026-07-06 on) :  6 completions / 13.7 days = 0.44/day
SINCE last completion (2026-07-19)     :  0 completions / 33 days
```

And the decisive per-run attribution — is the late era slow because runs got
bigger, or because they got stopped? Wall-clock duration of the four latest
completed runs vs. halt time attributed to each from `campaign_log.md`:

```
run      wall_h   halt_h   halted share
run_054   52.73    51.15      97%
run_057   35.37     0.00       0%   (brief mandated manual --once stepping)
run_058   23.11    21.71      94%
run_059   30.99    30.70      99%

TOTAL    142.20   103.56      73%
```

A run that does ~15 minutes of actual pipeline work (the June-era median) was
taking a day and a half of calendar time in July, and 73–99% of that was the
machine sitting halted, not doing research. **This is not a throughput
regression from added rigor — the June era's 30 completions produced zero
promotions, so the rigor added since (cost gates, prescreen, reactivation
gates) was correct and is not this epic's target.** The target is that the
system cannot survive its own operation once it hits a transient failure.

### The loop also cannot restart itself once idle — related, not this epic

`stages.yaml`'s terminal stages (`verdict_interpreter`, `campaign_review`)
both have `next: []`. `register_hypothesis()` (the only queue-append path for
a genuinely new hypothesis) has no in-pipeline caller — one `REGISTER:` line
exists in the log's whole history, from a manual CLI invocation. The queue
today is 3 `done` + 1 `blocked`, and has been since 2026-07-19. This is a
related but separate gap (queue self-refill), sequenced AFTER this epic — see
Relationship to other epics.

## Done when

1. **Satisfied by quarantine alone, 2026-08-23 — corrected from the original
   text.** A classified halt-recovery policy exists: transient failures (the
   classes measured above — `unhandled_exception` subtypes that are provably
   retry-safe, `component_execution_error` where the component is stateless)
   retry automatically with a bounded attempt count; a run that still fails
   is quarantined (marked, queue advances past it) rather than halting the
   whole campaign; anything not classified escalates to a human exactly as
   today. The taxonomy (S1) found exactly one evidenced retry-safe signature,
   and it was already handled at the stage level before this epic started
   (ledger A11) — there was never a second one to wire up at the campaign
   level, so "retry automatically" has no live target and stays unbuilt (S2b,
   explicitly parked on evidence, not on effort). "Quarantined... escalates to
   a human exactly as today" is fully built (S2a) and this criterion is
   satisfied by that half alone.
2. **Satisfied, with the same retry correction.** A loop-health block is
   emitted per campaign run (or per `--once` step): halt count, downtime
   hours, downtime share of span, cause breakdown, and which causes were
   auto-recovered vs. escalated. Consumed by `run_campaign.py` itself to
   decide quarantine-vs-escalate at the next halt (not retry-vs-escalate —
   same correction as #1), not only read by a human (F6/F3 — see the skill's
   instrument-shape rule). Built S3.
3. **Satisfied, epic-wide, not just per-story.** Bit-identity: no change to
   any recorded backtest metric, trade record, or verdict. This is pure
   orchestration around existing stage/tool invocations; a test proves output
   is unchanged when every classified failure is disabled (equivalent to
   today's behavior). S2a and S3 each proved this for their own story; S4
   proved it as one claim against the epic's actual pre-E-030 baseline
   (`842a2788`) by a full recursive sandbox-tree comparison.
4. **Satisfied, both suites, 2026-08-23.** Fast suites green throughout, every
   commit, independently verified. Slow suite run and confirmed 2026-08-23
   (`python run_tests.py --slow`, then trading-bot rerun standalone at
   `--timeout=300` after the default 30s/test budget aborted one test under
   machine load — the same known, pre-existing environment issue this whole
   epic's own commits document, not a code failure): trading-bot 409 passed /
   2 skipped / 0 failed, strategy-research 884 passed / 0 failed (recorder
   tests included under `--slow`). This epic never touched `trading-bot/` (the
   engine) or any data-fetching code, so this was a low-risk gap to have left
   open — but a Done-when criterion that names the slow suite explicitly does
   not get checked off on "low risk," it gets checked off on having actually
   run it.

## Stories

- [x] S1 — Characterize the halt taxonomy precisely: for each of the 14
      historical halts (this epic's own measured evidence) and any additional
      halts found on other run families, classify as
      retry-safe / quarantine-safe / must-escalate, with the reasoning. No
      code changes — this determines what S2 is allowed to automate.
      **Done 2026-08-22** (`3073ca7e`):
      `E-030/artifacts/s1_halt_taxonomy.md`. Of 127.0h halted, 37.2h (29%) is
      automatable and still live (20.4h retry-safe, 16.8h quarantine-safe);
      21.9h more was retry-safe and already fixed (A11); 21.0h is correctly
      must-escalate. The largest single halt (46.9h, 37% of all downtime)
      turned out unclassifiable — see S1.5 below, opened directly from this
      finding.
- [x] S1.5 — Durable halt record (not in the original story list; opened from
      S1's own finding that the retry/quarantine evidence S2 needs to decide
      on was being destroyed before anyone could read it). Two separate lossy
      points: `campaign_log.md`'s HALT line truncates `last_error` to 300
      chars at write time (`run_campaign.py:874-875`), and RUNBOOK.md
      section 4's own documented resume procedure has the operator null
      `last_error`/`flags` on every resume, with nothing archiving the value
      first — standard, sanctioned procedure, not operator error. Two pieces:
    - [x] **Piece 1 — done 2026-08-22** (`994157ec`): `halt_history` added as
          an accumulating field on `pipeline_state.yaml` itself (modeled on
          `completed_stages`/`audit_log`, the two fields on that same file
          that already accumulate instead of being overwritten — not a new
          artifact type). Appended at both `HALT` sites in `process_once()`
          before either resume step can touch `last_error`/`flags`. RUNBOOK.md
          section 4 annotated: the reset is unchanged and still correct, it's
          just no longer lossy. Pure addition, no existing key/artifact
          touched. Suites green: strategy-research 817 passed, trading-bot
          383 passed / 2 skipped.
    - [ ] **Piece 2** — decouple the `audit_log` attempt-counter from
          `counters.refinements_used` (RUNBOOK.md section 4.5's known
          crash-resume overwrite: `injected_context["refinement_attempt"]` is
          regenerated from the refinement-budget counter on every loop entry,
          so a same-counter re-entry overwrites rather than appends the
          `f"{stage_name}_attempt_{attempt_num}"` audit key). RUNBOOK
          explicitly forbids hand-bumping `refinements_used` to fix this
          cosmetically — needs its own, independent counter. This is why
          halt #14's provenance (S1) was undecidable: the intermediate
          attempt that would have proven it was silently overwritten.
- [ ] S2 — Implement the retry/quarantine policy in `run_campaign.py`,
      off-by-default disableable for a bit-identity test.
    - [x] **S2a — quarantine + escalate, done 2026-08-22.** The QUARANTINE half
          only, and the narrowing is deliberate rather than partial delivery.
          S1's R2: *"The one proven-retryable signature is an exact string match,
          and it is already implemented that way"* — the single evidenced
          retry-safe case (the `claude_agent_sdk==0.2.82` result-misclassification
          message) is already retried at the STAGE level in
          `_invoke_agent_with_yaml_retry` (ledger A11, `9bf2a4cf`). There is no
          second evidenced campaign-level retry-safe signature, so building retry
          machinery now would mean inventing a heuristic without evidence — the
          reason-code-keyed guessing R2 exists to forbid. Nothing was stubbed
          either. **Do not read this as "S2 done": S2b (retry) is unbuilt and
          stays unbuilt until a dispatch finds a genuine new retry-safe
          signature.**
          Quarantine-safe set, from S1's per-halt evidence and nothing else:
          `no_signal_artifact`, `component_execution_error` (both terminal:
          `status: done`, `outcome: quarantined_engineering_failure`), plus
          `component_gap` and `new_component_escalation` (re-queueable:
          `status: blocked_on_component:<name>`, no outcome — R9). Everything
          else escalates unchanged, `unhandled_exception` included (R2).
          Gated off by `orchestrator.halt_policy.quarantine_enabled: false`;
          flag-off proven byte-identical against this epic's own base commit
          `842a2788` by dumping every artifact the halt path touches (queue
          entry, `campaign_log.md`, `campaign_summary.md`, `halt_history`,
          `campaign_state.yaml`, `process_once`'s return) across all four
          quarantine-safe reasons plus `unhandled_exception` and diffing:
          12,343 bytes, zero differences outside wall-clock timestamps.
          R6's record extends `halt_history` (the queue's closed schema,
          `record_schema.QUEUE_ENTRY_SCHEMA`, structurally cannot hold it).
          R7 calls the existing `_mark_trial_invalidated` and adds no new
          trial-recording function. R11 escalates on flag ambiguity and logs it.
          Suites green: strategy-research 840 passed / 3 skipped (baseline at
          `842a2788` in the same worktree: 816 / 3, so +24 = exactly the new
          tests, zero regressions); trading-bot 381 passed / 4 skipped /
          26 deselected, untouched by this story.
          **One premise correction found while implementing** — see S2a's own
          note in `_apply_trial_accounting`: `new_component_escalation` does NOT
          fire before any backtest. `_route_escalate` is reachable only from
          `determine_post_verdict_route` / `determine_post_campaign_review_route`,
          both of which require `verdict_interpretation.yaml` and therefore a
          completed `protocol_execution`. A trial row generally DOES exist, and
          it must be left alone: it is a real measurement whose hypothesis then
          routed to "the engine needs a new piece" — a research routing decision,
          not an engineering failure of the measurement. Invalidating it would
          shrink N in the flattering direction. `no_data_touched` on the
          quarantine record is therefore measured per-run, never inferred from
          the reason code.
    - [ ] **S2b — retry.** Blocked on evidence, not on effort. Needs a genuine,
          reproducible retry-safe signature that is not already handled at the
          stage level. R3/R4/R5 are the standing discipline for whenever one
          appears: clear the previous attempt's flags (halt #5 is the proof a
          bare retry is not a retry), stop after the same reason code twice on
          the same run, and never stack a campaign-level retry on the two that
          `_invoke_agent_with_yaml_retry` already nests.
- [x] S3 — **Done 2026-08-23** (`5053148e`). "Consumed by the retry decision"
      (this story's own original wording) is not literally buildable — S2b
      stays unbuilt, nothing to decide between. Built instead:
      `campaign_record/loop_health.yaml`, re-derived from `campaign_log.md` +
      every run's `halt_history` on each `process_once()` step (halt count,
      downtime hours/share/median, a two-bucket `quarantine_safe`/`escalate`
      cause breakdown — a `retry_safe` bucket isn't observable at this layer,
      the one evidenced case is resolved inside `_invoke_agent_with_yaml_retry`
      before a halt is ever logged — and auto-recovered vs. escalated counts).
      F3's actual bar ("the loop can consume it, not only a human") is met by
      wiring it into the one real decision available: R4 ("same reason code
      twice in a row ⇒ stop auto-actioning, escalate," evidenced by halts
      #13/#14, both `component_execution_error` on `run_059`) extended from
      retry to quarantine — a run that hits the same quarantine-safe reason
      twice in a row now escalates on the second occurrence instead of being
      auto-quarantined again. Gate reused `quarantine_enabled` rather than a
      third flag (when quarantine is off, nothing can ever carry a repeat
      record, so a separate toggle would be dead config on inspection).
      23 new tests, including one asserting the block's pairing logic
      reproduces `measured_halt_cost.txt` verbatim from the real
      `campaign_log.md`. Suites green: strategy-research 866 passed,
      trading-bot 383 passed / 2 skipped.
- [x] S4 — **Done 2026-08-23** (`3eba6ba0`). Audited existing coverage first
      (S1.5/S2a/S3's own tests) rather than duplicating it, and in doing so
      corrected this epic's own record: `842a2788` is S1.5 Piece 2, not "the
      last commit before E-030" — `halt_history` was already present there
      (landed one commit earlier, `994157ec`), so it was never part of the
      epic-level bit-identity gap. Established the real delta by an AST-level
      function diff (`842a2788` → `55e812c0`): 11 functions added, 0 removed,
      2 changed, and with the flag off the entire delta reduces to the four
      `_write_loop_health()` calls — proven, not assumed, by a full recursive
      sandbox-tree comparison across 6 reasons, plus a companion test proving
      flag-off reaches none of the six S2a/S3 decision functions. Three
      regression fixtures replay real taxonomy evidence verbatim (real run
      IDs, real `last_error` text, real trial rows): halt #10/#12
      (retry-safe — proven to never become a halt at all, resolved at the
      stage level before `process_once()` is ever reached), halt #13
      (quarantine-safe — `run_059`, both of its real trial rows correctly
      marked `invalidated_artifact` per F6, never deleted), halt #4
      (must-escalate — `run_053`'s `kb_reactivation_violation`, escalates
      identically with the flag both off and on, proving R1's integrity list
      is never overridden). 18 new tests, 5 mutations killed in verification
      (each reverted). Suites green: strategy-research 884 passed, trading-bot
      383 passed / 2 skipped.

## Relationship to other epics

- **E-009** — this epic is S3/S4 of E-009, split out and re-scoped on
  measurement (see Why). E-009 keeps its two mechanical refactors
  (`STAGE_CONFIGS`/`skill_map` merge, `sample_split` override); its own
  Done-when should be edited to drop S3/S4 and point here.
- **Queue self-refill** (not yet its own epic — the loop's inability to
  restart after "queue exhausted," see Why) is the natural next step after
  this one lands, per the operator's confirmed sequencing (2026-08-21):
  halt recovery → queue self-refill → E-029 → E-027. Opening it as its own
  epic is future work, not done here.
- **E-029 / E-027** (trade-record fields / exit-cause attribution) — both
  still real, both sequenced after this and after queue self-refill. Once the
  loop runs unattended, verdict quality stops being academic; it isn't today,
  because nothing is running.

## Log

- 2026-08-21 — `new` → `planned`. Opened from a `research-system-evolution`
  review, split out of E-009 S3/S4 on measurement. Includes one self-correction
  made and reported during the same review: an earlier claim of "4 completed
  runs ever" was wrong (built from `campaign_log.md` alone, which only covers
  the queue-driver era) and was corrected to 36, using `pipeline_state.yaml`
  as the primary record instead. The corrected numbers strengthened rather
  than weakened the case for this epic — see "Measured: throughput collapse"
  above.

- 2026-08-22 — **S1 approved by the operator** (characterization only, no
  code). State stays `planned` until S1 is actually dispatched — approval
  recorded here so the next session can dispatch without another round-trip.
  Same review round: two denominator corrections from a follow-up invocation's
  reconciliation, both verified by execution before landing — the prose above
  said "(56 runs)" where the true figures are 58 state files / 46 with
  timestamps (the 36-completions figure was and is correct), and
  `measure_verdict_repetition.py`'s header label now discloses its
  `root_cause.mechanism_failure` fallback instead of claiming all counted runs
  carry `primary_failure_mode` (36 carry the field; 1 counted via the
  fallback). The companion recommendation to flip P4_ts_trend to `ready` was
  **held by the operator's reviewer**: the KB reactivation clause for the
  parent still has three unmet conditions — the trade-floor ruling
  (`ts_trend_daily_v1.json:132` = 1 vs `campaign_config.yaml:120` = 5, both
  verified live at HEAD this date), a machine-evaluable pass_rule for the
  parent (the existing rule covers only the terminally-closed ER variant and
  resolves `legacy_not_evaluable`), and the daily-panel correlation-adjusted
  breadth count. Only the data condition (a) is dead. Flipping `ready` with
  (c) unmet would arm the queue to produce another ungated measurement.

- 2026-08-22 (same day) — **S1 done** (`3073ca7e`), **S1.5 opened and its
  Piece 1 done** (`994157ec`). S1.5 wasn't in the original story list —
  S1 itself surfaced it: the largest halt in the record (46.9h, 37% of all
  downtime) turned out unclassifiable because the evidence a retry/quarantine
  policy would need was being destroyed before it could be read (log-line
  truncation + the resume procedure's own documented `last_error=None`
  reset, with no archive). Piece 1 (the `halt_history` accumulating field)
  is done; Piece 2 (the audit-log attempt-counter decoupling) is scoped and
  next. State stays `planned` — S2/S3/S4 are unstarted and this remains a
  prerequisite for them, not a completion of the epic.

- 2026-08-23 — **Epic done.** S1.5 Piece 2 (`842a2788`), S2a (`83f8f1b0`), S3
  (`5053148e`), S4 (`3eba6ba0`, cherry-picked from `c8d2c18d` after `HEAD`
  moved) all landed this session, each independently verified by the director
  against real suite runs and real diffs before merge — not taken on any
  dispatch's own narrative. **State moves to `done` with S2b explicitly
  parked**, not silently dropped: it is blocked on evidence (a genuine,
  reproducible campaign-level retry-safe signature) that does not exist
  today, and Done-when #1/#2 were both corrected in place, this same session,
  to say so plainly rather than leaving the original "retry-vs-escalate"
  wording to mislead a future reader into thinking it shipped.

  Two things found and fixed that were not part of any story's original
  scope, both from a director-run bug hunt across the session's own commits
  (`f0ff0432` fixed the one file that broke): three MORE test files carried
  the identical git-environment-leak vulnerability class
  (`test_dual_writer_guards.py` — one call is `git init --bare`, an even
  closer match to the incident's own mechanism — `test_holdout_date_gate.py`,
  `test_s4_union_merge.py`), fixed once, centrally, in
  `tests/conftest.py`'s existing autouse sandbox fixture rather than
  patching four files individually (`39d02ded`). `_repeat_quarantine`'s
  adjacency-only check was also traced for the same class of gap and found
  to be deliberate, disclosed, already-tested behavior — not touched.

  Two provisioner-level findings, disclosed by two consecutive dispatches
  (S3 and S4) on this same epic, neither fixed here (outside this epic's
  scope, both explicitly noted as findings for whoever owns worktree
  provisioning): agent worktrees were provisioned from a stale base
  (`a56986e9`, several days old) rather than the session's actual current
  HEAD — both dispatches caught it and branched off the correct commit
  explicitly rather than working from what they were given; and worktree
  data-cache fixtures are incomplete in a way that produces failures, not
  just skips, on a fresh worktree's first run (S4's report: a 265-row BTCUSDT
  stub self-poisoning two unrelated tests in `test_a851a_prescreen_
  integration.py`).

  Every commit's suites independently re-verified by the director on the
  actual merged tree, not the worktree's own report: fast suites green on
  every commit (final state: trading-bot 383 passed / 2 skipped;
  strategy-research 884 passed); slow suite run and confirmed this same day
  (Done-when #4): trading-bot 409 passed / 2 skipped, strategy-research 884
  passed (recorder tests included under `--slow`, no separate count from the
  fast run since none of this epic's tests are marked `slow`).

- 2026-08-23 (unrelated to the epic itself; recorded here only because the
  2026-08-22 entry above is where the P4_ts_trend trade-floor conflict was
  last documented) — the operator ruled that day that
  `config/campaign_config.yaml:141`'s A3.4 floor of 5 governs over
  `protocols/ts_trend_daily_v1.json:132`'s then-value of 1; that file's
  `promotion.min_trade_count_gte` was changed 1 → 5 to match, resolving
  condition (b) of `campaign_knowledge_base.yaml`'s
  `p4_sma_trend_longonly_daily_auto` `reactivation_condition`. Conditions (c)
  (machine-evaluable pass_rule) and (d) (correlation-adjusted daily-panel
  breadth) were then worked: (d) measured n_eff ≈1.66 (all-19) / 1.69
  (primary 17, BTC/ETH excluded as an asset-level contamination) against a
  required ≥3.0 (derived from the project's own standing ≥30-independent-
  episode Sharpe-quoting floor and the brief's conservative low-end
  transitions estimate) — **not adequate**, so (c) was not authored past a
  draft that documents the shortfall rather than a ratifiable rule. Full
  package: `strategy-research/briefs/artifacts/p4_daily_reactivation_20260823/`.
  P4_ts_trend's queue status is unchanged (still not `ready`) pending the
  operator's disposition on the power finding — this does NOT reopen or
  extend this epic's own scope or Done-when.

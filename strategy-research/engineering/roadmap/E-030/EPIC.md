# E-030 — Halt recovery + a loop-health instrument

**State:** planned
**Owner:** Jeremy
**Updated:** 2026-08-21

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

1. A classified halt-recovery policy exists: transient failures (the classes
   measured above — `unhandled_exception` subtypes that are provably
   retry-safe, `component_execution_error` where the component is stateless)
   retry automatically with a bounded attempt count; a run that still fails
   is quarantined (marked, queue advances past it) rather than halting the
   whole campaign; anything not classified escalates to a human exactly as
   today.
2. A loop-health block is emitted per campaign run (or per `--once` step):
   halt count, downtime hours, downtime share of span, cause breakdown, and
   which causes were auto-recovered vs. escalated. Consumed by
   `run_campaign.py` itself to decide retry-vs-escalate at the next halt, not
   only read by a human (F6/F3 — see the skill's instrument-shape rule).
3. Bit-identity: no change to any recorded backtest metric, trade record, or
   verdict. This is pure orchestration around existing stage/tool
   invocations; a test proves output is unchanged when every classified
   failure is disabled (equivalent to today's behavior).
4. Fast and slow suites green.

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
- [ ] S3 — Implement the loop-health instrument (block emitted per run/step,
      consumed by the retry decision) and wire it into `process_once()`.
- [ ] S4 — Bit-identity test + the classification's regression fixture (one
      historical halt of each class, replayed against the policy).

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

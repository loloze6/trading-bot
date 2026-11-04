# Stop 23: The route and the run's end

## Speech (verbatim)

**Stop 23 of 29: The route and the run's end.** Open on the side: `run_phase1_research.py`, `run_campaign.py`, `docs/RUNBOOK.md` (§3, §4).

**In one sentence.**
The route is the run's last decision: after the record is written, it either pauses the run for a person or ends it with the grid's verdict; the campaign runner then files that ending in the queue, sets the run aside, or stops the campaign until a person resumes it.

**Why it exists.**
A run must end in one known state the next step can trust: finished with a verdict, waiting for a person with a named reason, or parked (set aside while a missing piece is built). Without it, a paused run could restart unnoticed, a profitable variant could slip past the operator, or spending could continue after a fault.
The verdict comes from the grid (the pass/fail table of criteria written before the run) and nothing else, so no later story can change it.

**What comes in, what goes out.**
- In: the grid's status (validated, refuted, inconclusive); the profit-bars evaluation (the campaign-wide profitability thresholds, stop 20); any component crash from the backtests; the operator's holdout decision, when one is awaited; the campaign memory, for the review count.
- Out: the run's state file set to its ending; the run listed in the campaign state with one diagnostics row; for a pause, the queue entry marked paused with its reason, a halt record on the run, a HALT line in the campaign log; for a park, the entry marked waiting for a component or for data.
- Next: decide-next, for a finished or parked run (stop 24); the campaign review, when due (stop 26); the operator, for a pause.

**What happens here, step by step.**
1. After the record-keeping stage, a strategy component that crashed during a backtest pauses the run: an engineering fault, not a finding.
2. Otherwise, a variant that cleared every profit bar pauses the run for the operator. On resume, the run re-enters the record-keeping step and this route, which sees the stop was already raised. A "continue" decision goes on to step 4; a "spend" goes to the holdout test (the sealed final period, stop 27).
3. An operator re-run on another fold (a fixed set of test months) ends here, with no verdict.
4. Otherwise the route reads the grid's status and ends the run "completed", with that status as its ending. The run is recorded in the campaign state.
5. If at least six counted runs have finished since the last campaign review, the run goes to the review first.
6. The campaign runner reads the run's state. A parked run: the queue entry becomes "waiting for component" or "waiting for data", decide-next still runs, and the campaign continues.
7. A failed run, a spent budget or a pause: the runner names one reason from a fixed, ordered list (the first match wins), marks the entry paused, records the halt and stops the whole campaign.
8. A finished run is checked against a readable status file, then handed to decide-next.

Three ways back after a stop:
- Resume: the operator fixes the cause and clears the run's paused state. The runner checks the pause is truly resolved (after a profit-bars stop, that a valid holdout decision exists), then continues the same run where it stopped.
- Unpark: once the component is built or the data fetched, the same run restarts at the stage where it parked. It is refused while a named component is still missing.
- Relaunch: a crashed run starts again fresh; the old folder is kept.

Example: run_102 ended `status: completed`, pending `completed_refuted` (its state file's first lines, quoted at stop 00). run_102's own `pipeline_state.yaml` is not in this checkout.

**What is switched off or not used here.**
- The older route (promote, kill, refine, pivot, escalate, and the pause on an inconclusive grid) is not reached under the current flags: skipped at `run_phase1_research.py:5448-5449`. The classifier still names the inconclusive pause (`run_campaign.py:1644`).
- Quarantine, which would let the queue move past four engineering-fault reasons, is off (`campaign_config.yaml:122`), so every pause stops the campaign.
- RUNBOOK §3 marks two reasons retired (`:675`, `:699`); the classifier still names them (`run_campaign.py:1544`, `:1575`).
- In this checkout the committed switchboard has the switches this route relies on off (`campaign_config.yaml:388-389`, `:699-700`); the tour's current flag set, the operator's uncommitted edit, has them on.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Route after record | `run_phase1_research.py:20576-20611` | Profit-bars stop (`:20584-20585`), holdout unlock (`:20589-20590`), refold end (`:20593-20595`), grid route (`:20599-20605`), review (`:20610-20611`) |
| Grid route | `run_phase1_research.py:5403-5462` (`determine_post_specialist_readers_route`) | Component-error pause `:5435-5444`; routing retired `:5448-5449` |
| Ending | `run_phase1_research.py:6649-6666` (`_route_retired_idea_status`); `:5683-5684` | `completed_validated` / `completed_refuted` / `completed_inconclusive` |
| Campaign state | `run_phase1_research.py:6627-6646` (`_record_run_in_campaign_state`) | `runs`, one `diagnostics_log` row, idempotent |
| Review due | `run_phase1_research.py:7867-7882` (`_retired_review_route`), `:7759-7778`, `:7751-7756`; `campaign_record/campaign_state.yaml:641` (committed copy, up to run_097: 6) | Cadence, digest, handoff |
| Refold end | `run_phase1_research.py:5218-5230` | `completed_refold` |
| Mark completed | `run_phase1_research.py:20677-20701` | `status: completed`, `pending_stage` = ending |
| Park | `run_phase1_research.py:6605-6624` (`_park_run`); callers `:18944`, `:19458`, `:19509`, `:20371`, `:20419` | Parked marker, `resume_stage` |
| Profit-bars stop and unlock | `run_phase1_research.py:15570-15623`, `:7515-7557` | Stop 20 |
| Runner after the loop | `run_campaign.py:4662-4666` (park first), `:4668-4783` (pause, quarantine branch, HALT), `:4785-4811` (checks at DONE) | |
| Hard pause | `run_campaign.py:1706-1772` (`_hard_pause_reason`) | Failed, budget, review terminate, wishlist, paused |
| Classifier | `run_campaign.py:1494-1703` (`_classify_human_pause`) | 35 outcomes (34 reasons and "unclassified"), first match wins |
| Halt records | `run_campaign.py:1775` (`_append_halt_history`), `:333-351` (`_halt_retired_routing`) | `halt_history`, `paused:<reason>`, HALT line |
| Park entry | `run_campaign.py:4949-4994` (`_park_entry`), `:4937` (`_parked_note`) | `paused:waiting_for_<kind>`, decision under `parked/park_<n>/` |
| Resume | `run_campaign.py:2197-2375` (`resume_paused_entry`; holdout check `:2359-2367`), `:2378` (`_clear_run_halt_flags`) | Same run continues |
| Unpark | `run_campaign.py:2392-2469` (`_unpark_entry`) | Under the campaign lock; entry `ready` |
| Relaunch | `run_campaign.py:2496-2624` (`_relaunch_entry`), `:2474` (allowed reasons) | Fresh run; old run orphaned |
| Commands | `run_campaign.py:5939-5950` | `--resume`, `--unpark`, `--relaunch` |
| RUNBOOK §3 | `docs/RUNBOOK.md:581-742` (table `:671-739`, 66 rows) | Every halt reason and its fix |
| RUNBOOK §4 | `docs/RUNBOOK.md:743-1089` (reset `:743-883`, unpark `:884-930`, relaunch `:931-964`; `:965` retry-analyst, stop 21; `:1015` approval, stop 24; `:1055` feed waits) | How to come back |

Remarks: send them as "stop 23: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

(Checkout note: no `SR/runs/run_102/`; the committed switchboard has `verdict_routing_retired`, `decide_next`, `profit_bars_every_backtest` off. Notes judge the mechanism under the tour's flag set.)

### (1) Design and mechanism

1. The route is short, ordered and closed: component-error pause, profit-bars stop, holdout unlock, refold end, `completed_<idea_status>`, review cadence (`RP:20576-20611`, `:5403-5462`, `:6649-6666`); the endings are a closed set (`:5683-5684`), the status file is re-read at DONE and a mismatch halts (`RC:295-310`, `:4806-4811`), and the campaign-state row is idempotent on a resume (`:6627-6646`). A run cannot end in an unnamed state. Sound.
2. The halt policy is the autonomy ceiling, stated plainly: with quarantine off (`campaign_config.yaml:122`) every reason `_hard_pause_reason` returns stops the whole campaign (`RC:4770-4783`), and every way back is a hand operation: `--resume` after the operator edits `pipeline_state.yaml` per RUNBOOK §4 (`:743-883`, 140 lines of reset steps) and the runner confirms the state is no longer paused (`:2349-2357`); `--unpark` after a human built the component (`:2439-2448`); `--relaunch` for two crash reasons (`:2474`). The one run state that does not stop the loop is a park (`:4662-4666`, `_park_entry :4949-4994`), where decide-next still runs so the campaign moves to another lineage. "Run autonomously and continuously" therefore means: until the first of about thirty pause reasons, then wait. That is the operator's D-071/E-030 choice; the mechanism implements it faithfully.
3. The classifier (`_classify_human_pause :1494-1703`) is a hand-ordered first-match over sticky flags that are "never set back to False in code" (`:1503-1509`, its own comment), which is why its order is load-bearing and commented at every branch. Under the live flags the reasons that can fire are a minority: `component_execution_error`, `profit_bars_reached`, the holdout-unlock family, `variant_shape_invalid`, `variant_config_error`, `forecast_rule_violation`, `config_deviation`, `config_replay_mismatch`, `variant_gate_insufficient`, `campaign_review_terminate`, the three halt flags, `kb_reactivation_violation`, plus `budget_breaker` and `unhandled_exception`. The rest name retired stages (`no_signal_artifact`, `anti_adjacency_gate_exhausted`, `pass_rule_evaluation_disagreement`, `inconclusive_grid`, `provisional_promote_*`, `new_component_escalation`, `data_block_hitl`, `stale_escalation_unclaimed`). RUNBOOK §3's 66 rows document all of them; a new joiner reads a table twice the size of the live one.
4. The halt record is durable by design and for a documented reason: `_append_halt_history` keeps the untruncated `last_error` and the flags because a 46-hour halt once left no recoverable cause (`:1775-1800`). The quarantine branch (`:4683-4769`) reads that history for its repeat rule. Good engineering; with the flag off it is a record for the operator only.
5. Two run lists exist: `campaign_state.yaml` `runs` (55 committed, every run the retired routing recorded too) and the memory's 24 entries (stop 22a). The review cadence counts the memory (`:7759-7778`), the DSR counts the state's trial rows (stop 20), the summary reads the state. Three records answer "how many runs" differently; each is right for its reader.
6. Parks are placed before any backtest (`RC:2401-2403`), so a parked run never loses a trial row, and `--unpark` refuses while a named class is still undefined (`:2439-2448`) and restarts at the marker's `resume_stage` (`:2449-2451`). The component request the park wrote has no status (stop 10 note 1.4), so "built or not" is checked by importing the class, not by the request file. Correct and minimal.
7. The refold terminal (`completed_refold`, `:5218-5230`, `:20593-20595`) ends an operator re-run with no verdict and no decide-next; the only path that re-tests the same config on another fold is the operator's command. Consistent with stop 06.
8. A validated run with no passing bars and a refuted run with a passing variant end the same way for the queue (`completed_<status>` then DONE); the bars stop pauses only on a pass (stop 20 note 1.4). The route never combines the two judges; the operator does, at the pause or in the review.

### (2) Legacy or simplifiable (leads)

1. The flag-off half of `determine_post_specialist_readers_route` (`RP:5450-5462`: the inconclusive pause, `_resolve_verdict_fields`, `_dispatch_verdict_route`) and `_GRID_IDEA_STATUS_ROUTING`'s labels (stop 19 lead 2.2).
2. `_classify_human_pause`'s retired reasons (note 3) and the artifact-based tail (`promotion_audit.yaml`, `holdout_result.yaml` status, `decision.yaml` `component_gap`, `escalation` target, `refinement` decision; grep lines `:1612-1646` relative), `_hard_pause_reason`'s `stale_escalation_unclaimed` (`:1718-1719`) and the `campaign_review.yaml` wishlist evaluation (`:1739-1761`); RUNBOOK §3 rows marked retired (`:675`, `:699`) still classified (`:1544`, `:1575`).
3. The quarantine branch (`RC:4683-4769`, about 85 lines with `_flag_ambiguity`, `_repeat_quarantine`, `_apply_trial_accounting`, `_blocked_component_name`, `_QUARANTINE_SAFE_REASONS`, `_REQUEUEABLE_QUARANTINE_REASONS`): off; stop 28.
4. The legacy continuation check (`:4792-4805`, `continuation_child`, `_LEGACY_MINTING_ROUTERS`, `_legacy_continuation_blocker`) and `_COMPOSITION_FAULT_REASONS` / `_is_composition_run` (`:4669-4673`): refusals of shapes no live run makes; stop 02 lead 2.7.
5. `_relaunch_entry` (`:2496-2624`, 130 lines) for two reasons, with `ORPHANED_README` and the queued-cards accounting (`:2481-2493`): kept if crashes recur; a smaller command if not.
6. `resume_paused_entry`'s branches for `FLAG_PREFLIGHT_HALT`, `LAUNCH_EXCEPTION_HALT`, `data_block_hitl` (`:2222-2240`, `:2340-2347`): three bespoke resumes beside the generic one.

### (3) Disagreements between the speech and the element

1. Step 7, "names one reason from a fixed, ordered list (the first match wins)": two lists in order, `_hard_pause_reason` (failed, budget, review, wishlist) then `_classify_human_pause` (`:1706-1772`, `:1494-1703`); correct. "35 outcomes (34 reasons and unclassified)": not recounted here; the live subset is about fifteen (note 3), which the speech does not say.
2. Step 6, "A parked run: ... decide-next still runs, and the campaign continues": `:4662-4666`, `:4982-4985`; correct, and the parked entry is persisted only after the decision is on disk (`:4959-4963`), which the speech omits.
3. Step 5, "If at least six counted runs have finished since the last campaign review": cadence from `campaign_state.yaml:641` (6), runs counted in the memory without a fault (`:7759-7778`); correct; a run with no memory entry raises rather than skipping the review (`:7767-7772`), fine.
4. "Three ways back": `--approve` is a fourth command (`:5944-5947`) for held entries, not pauses; the speech is right to leave it to stop 24.
5. Section 6: "skipped at `:5448-5449`": verified. "The classifier still names the inconclusive pause (`:1644`)": verified. "RUNBOOK §3 marks two reasons retired (`:675`, `:699`); the classifier still names them (`:1544`, `:1575`)": `no_signal_artifact` and `anti_adjacency_gate_exhausted`; verified. "Quarantine ... off (`:122`)": verified.
6. Reading map verified: `RP:20576-20611` (`:20584-20585`, `:20589-20590`, `:20593-20595`, `:20599-20605`, `:20610-20611`), `:5403-5462` (`:5435-5444`, `:5448-5449`), `:6649-6666`, `:5683-5684`, `:6627-6646`, `:7867-7882`, `:7759-7778`, `:7751-7756`, `:5218-5230`, `:20677-20701` (stop 05b), `:6605-6624` (callers not opened), `:15570-15623`, `:7515-7557` (stop 20); `RC:4662-4666`, `:4668-4783`, `:4785-4811`, `:1706-1772`, `:1494-1703`, `:1775`, `:333-351`, `:4949-4994`, `:4937`, `:2197-2375` (`:2359-2367`), `:2378`, `:2392-2469`, `:2474`, `:2496-2624` (head and tail), `:5939-5950`; `RUNBOOK.md:581`, `:671-739` (66 rows), `:743`, `:884`, `:931`, `:965`, `:1015`, `:1055`, `:1090`; `campaign_state.yaml:641`.

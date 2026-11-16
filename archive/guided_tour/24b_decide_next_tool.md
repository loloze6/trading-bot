# Stop 24, part b: The decide-next tool

## Speech (verbatim)

**Stop 24 of 29, part b: the decide-next tool.** Open on the side: `tools/decide_next.py`, `tools/novelty.py`, `tools/research_folds.py`, `tools/composition.py`, `workflow_artifacts/schemas/decision_record.schema.json`. Part 24a covered the runner's side: when it calls this tool and what it does with the answer.

**In one sentence.**
Decide-next is the campaign's chooser: after a run, it lists every follow-up idea the analyst proposed, removes repeats and ideas that cannot run, ranks the rest, picks one (or asks for more ideas, or stops), and writes the pick as a new brief.

**Why it exists.**
A campaign that runs by itself must choose its next test in a way a person can check. Without a fixed rule it could repeat a test, retest an idea on the months where it was noticed, or pick for reasons nobody can read back. Here the rule is code, and every candidate is written down with its reasons.

**What comes in, what goes out.**
- In: campaign memory (one entry per run, stop 22); the analyst's proposals (follow-up ideas per lens, a reading angle, stop 21); each source run's config, block manifest (which parts of the config are the idea), test settings and brief; the queue (the to-do list, stop 02); the folds.
- Out: a decision record and, for a picked idea, a candidate brief's text. The runner writes both files (24a).
- Next: step 1a (the idea-writing step) reads the brief when its line runs.

**What happens here, step by step.**
1. If a queue line is in progress or ready, it is the pick; nothing new is made.
2. Otherwise every proposal not yet on the queue is a candidate, named `<lens>-<run>-<n>` after its own run, clashing with no line or brief file.
3. A follow-up gets its own fold (a fixed set of test months): drawn at random among folds A to D the source run is not on, seeded by the candidate's name so the draw replays, keeping folds where the coin has data in every window. No fold left: refused.
4. Feasibility, by kind. A side finding (something the analyst noticed, its test pre-filled) starts from the source config with its change, or from a full config it carries, which waits until every piece it uses exists. A patch (an edit of the source config) must still apply and fit the manifest. A regime piece is refused; a missing data feed makes it wait.
5. Repeat check: config fingerprint, coins, bar size and test windows form a key; a key already in memory is a repeat. With a drawn fold, the same config, coins and bar size on any other windows is a repeat too: a re-run on a new fold is the operator's command.
6. Cost: windows times 3 variants times coins, in backtests.
7. Duplicates collapse into one. The rest rank by the analyst's confidence score, then fewer backtests, then name; a tie is declared.
8. The pick: a combination of proven pieces when that rule fires (two or more on one bar size, not yet combined), behind running and operator lines; else step 1's line; else the top candidate; else a request to step 1a for more ideas on each open brief; else a stop.
9. The record keeps the trigger, input fingerprints, both rules' states, every candidate with its reasons, and the pick.
10. The brief copies the source's brief keys and test settings (on the new fold), writes the goal in code, and carries the claim, start config, manifest, source and observations. A fold follow-up keeps its source's criteria when all are menu items; otherwise step 1a chooses.

Example, from stop 01's reading of forecast_power-run_102-2: a side finding; fold C drawn among A, C and D (run_102 was on B); criterion kept, forecast IC (rank correlation of forecast and later return) at 24 hours; both weights changed; ten observations. run_102's decision_record.yaml and retry_1/ are not in this checkout.

**What it costs and how long it takes.**
No AI call: code only (`tools/decide_next.py`, 2,832 lines).
Recorded cost basis: 10.2 seconds per backtest, 3 variants (`decide_next.py:134-139`).

**What is switched off or not used here.**
- The older family lookup (exclusion digest) is recorded for information; it never refuses.
- Extra ideas at step 1a are off: no new waiting ideas are made to rank.
- The built-in copy of the scheduler rule: the runner passes its own.
- My grep found no code reader of the brief's source observations outside this tool and tests.
- This checkout's committed switch file reads decide-next and its switches as off; the states here are the tour's flag set (stop 03a).

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Purpose and order | `tools/decide_next.py:1-107`; imports `:108-126` | Docstring: loader, three pure steps, what it never does |
| Constants | `tools/decide_next.py:128-215` | `AGENT_PRIORITY` 999, `N_VARIANTS` 3, `SECONDS_PER_BACKTEST` 10.2, brief statuses, R2 limits (`:173-202`), `OPERATOR_APPROVAL_STATUS` `:207` |
| Hashes, engine pieces | `tools/decide_next.py:226-330` | `config_sha256`; component classes and ops read from TB source (`known_component_classes :255`, `known_ops :290`) |
| Feeds | `tools/decide_next.py:332-537` | Feed registry; `requires_feed_gate :501` |
| Patch | `tools/decide_next.py:539-616` | `resolve_patch :589` |
| Base variant, key aliases | `tools/decide_next.py:617-641` | `novelty_key`, `_exact_index` from `tools/novelty.py` |
| Queue and brief helpers | `tools/decide_next.py:644-1022` | Brief owner, `[obsolete]` title, queued cards, exhausted answers `:892`, empty-R2 streak `:914`, holds |
| Loader | `tools/decide_next.py:1024-1171` | `load_inputs`; memory, registry, proposals per run, briefs, cards, flags as kwargs |
| Run windows, merges | `tools/decide_next.py:1173-1226` | `_memory_run_ranges`, `_observable_inputs`, `_composition_checker` |
| Combination (R1) | `tools/decide_next.py:1228-1575`; `tools/composition.py:518`, `:683`, `:723`, `:834`, `:992` | `_r1 :1423`, `composition_brief :1515`; variants, record, failure, returns, check |
| Notes | `tools/decide_next.py:1576-1611` | `_digest_advisory`; D-201 note `_same_config_other_fold_note :1597` |
| One candidate | `tools/decide_next.py:1612-1874` | `_candidate`: name, collisions, fold, patch, side finding (D-201 wildcard `:1759-1768`), sketch, cost, eligibility |
| Fold draw | `tools/decide_next.py:1876-1947`; `tools/research_folds.py:272-318` | `_fold_assignment_for`, `_fold_data_reason`; `draw_seed`, `draw_fold` (D-123) |
| Side finding start | `tools/decide_next.py:1949-2008` | `side_finding_start` |
| Config vehicle | `tools/decide_next.py:2010-2136` | `config_vehicle_reasons :2021`, `slim_vehicle`, `component_request_rows :2093` (D-162) |
| Review, warnings | `tools/decide_next.py:2138-2178` | `_side_finding_review`, `class_name_warnings` |
| Card, pre-ruling items | `tools/decide_next.py:2180-2254` | `_card_candidate`; `_legacy_no_vehicle_candidate` (D-151) |
| More ideas (R2) | `tools/decide_next.py:2256-2332` | `_r2`: `<owner>__more_<n>` |
| Collapse, rank | `tools/decide_next.py:2334-2403` | `_collapse`, `rank_key :2389` (D-194), `_tied_with` |
| Scheduler mirror | `tools/decide_next.py:2405-2423` | `_operator_entries`, `select_entry_rule` |
| Decide | `tools/decide_next.py:2426-2580` | Candidates `:2443-2471`; R1 `:2478`; scheduled `:2492`; top `:2499`; R2 `:2522`; stop; record `:2553`; retired-field refusal `:2577` |
| Criteria, fold protocol | `tools/decide_next.py:2587-2624` | `_criteria_for_child` (D-121), `fold_protocol` |
| Source observations | `tools/decide_next.py:2630-2643` | D-205 |
| Candidate brief | `tools/decide_next.py:2646-2832` | Five keys `:2664-2665`; goal; fold windows `:2688-2702`; claim and start config; patch `:2774-2800`; criteria `:2805-2811`; observations `:2813-2815`; prose |
| Exact key | `tools/novelty.py:186-208`, `:250-283` | `novelty_key`, `exact_index`, `window_free_key`, `matches_on_other_windows` |
| Record schema | `workflow_artifacts/schemas/decision_record.schema.json` | Nine required keys; applied by file stem at save |

Remarks: send them as "stop 24b: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

A regime piece is refused. - why ?? 
Here we should ensure that ideas arounf régime are tested
 
I find it risky to possibly delete or merge ideas here. We could loose useful ideas without even knowing. I would rather prefer ensure an entry is controlled before writing than treating recorded and queued ideas

## Inspector notes

(Checkout note: no `SR/runs/run_102/`, so `decision_record.yaml` and `retry_1/` are not checkable; the candidate brief of stop 01 is committed and was read there.)

### (1) Design and mechanism

1. Decide-next is pure, deterministic and fully recorded: the same inputs, clock and trigger give the same record (`decide_next.py:2426-2436`), every candidate is listed with its reasons, the inputs are fingerprinted (`:2555-2566`), the fold draw is seeded by the candidate id (`:1888-1891`), retired fields are refused (`:2577-2579`). For "a person can check" this is the right construction, and the record is the one file in the pipeline where the loop explains a choice.
2. What the choice rests on is thin. The rank is `confidence_real` descending, then backtests ascending, then candidate id (`rank_key :2389-2395`); `confidence_real` is the analyst's own in-run window agreement in four steps, 0 to 3 (stop 21b note 1.3), and the other two score fields were dropped (D-194). With most proposals at the same step, the order falls to cost, which is `windows x 3 x coins` for every side finding of the same source (`N_VARIANTS :134`), and then to the id string, where the lens name decides (`forecast_power` sorts before `trade_efficiency`). The record declares the tie (`:2503-2510`), which is honest; the fact is that which idea gets the next run and its 8 USD is, between tied candidates, alphabetical. The operator's decisions 4 and 6 (no lineage term, no other score) made it so.
3. The pool never ages: every proposal of every memory run stays a candidate until a queue entry names it (`:2440-2454`), re-drawn and re-checked each pass. A run_070 proposal competes with run_102's on equal terms; with a cap of 2 side findings per reading and 24 memory runs, the pool can hold dozens of candidates of which the top is re-elected at every DONE. No decay is the operator's choice (decision 6); the consequence is that the loop's next idea is the best-scored of the campaign so far, not of the last run.
4. Novelty is exact (stop 16 note 1.2) plus D-201: a side finding with an empty vehicle (today's strategy, unchanged) is a REPEAT when the same config, coins and bar size were measured on any windows (`:1761-1768`, `novelty.py:250-283`), so "confirm this claim on another fold" is never a candidate; the refold command is the operator's. That closes the loophole the fold discipline would otherwise open, and it means every automatic child carries a config change, which is what stop 15 note 1.3 observed: the lineage walks weights because a child must change something.
5. The fold draw excludes the source run's folds only (`_fold_assignment_for :1876-1897` passes `run_id` alone to `draw_fold`): stop 06 note 1.1 confirmed at the call site. `_fold_data_reason` (`:1900-1947`) refuses a fold the coin has no data on, by the gate's own layer-1 coverage, without the warm-up rule (its docstring says so, `:1912-1915`): the gate can still exclude the child's early windows (stop 17 note 1.4).
6. The brief it writes is the one stop 01 read: five keys copied (`:2664-2665`, no `scope`), a code-built goal, the source's criteria when all are menu ids (`_criteria_for_child :2587-2606`, D-121: the lineage's judge is constant, stop 08 note 1.4), the fold's windows (`fold_protocol :2609-2624`), the claim, start config and manifest, and the source run's observations verbatim (`source_observations :2630-2643`, D-205; stop 01 note 1.9's 443 lines). The brief is the loop's handover and it carries everything the analyst recorded, read or not.
7. R1 is built, on, and has never fired: it needs two forecast blocks on one bar size (`:2478-2491`, docstring `:84-96`), and the registry holds one. `composition.py`, `composite_cache.py`, the residual-IC composite and the grid's profit-bars cell are all its machinery (stops 19, 22b). The operator's stop-12 remark that the combined-block design is not agreed stands against about 1,500 lines of armed code; one more block on 1d and a composition run is minted at priority ahead of every agent entry (`:2484-2491`).
8. R2 ("more ideas on an open brief") is the loop's only way to leave a lineage: it fires when nothing is scheduled and nothing is eligible (`_r2 :2266-2332`), bounded by two empty requests per brief. With one open operator brief and the pool of proposals usually non-empty, R2 is rare; the loop prefers refining the current strategy to asking 1a for a new one (stop 21a note 1.4).
9. Cost figures are stale and harmless: `SECONDS_PER_BACKTEST = 10.2` from a 2026 measurement (`:137-139`) against about 40 s per window on run_102 (stop 18 note 3.4); `N_VARIANTS = 3` against the four variants every run makes (stop 15). Both are recorded "for the reader" and the rank uses the backtest count only (`:2389-2395`), so the order is unchanged; the record's cost line is wrong by a factor of four.

### (2) Legacy or simplifiable (leads)

1. `_legacy_no_vehicle_candidate` (`:2180-2254` region, D-151) for proposals written before the vehicle rule; `_digest_advisory` and the exclusion-digest family lookup (`:1576-1611`; information only; the digest is dead with a memory present, stop 07 lead 2.6); `_fold_in_run_merges` and `_merge` (`:2338-2358`, fed by `side_finding_merges.yaml`, whose writer has no caller, stop 21b lead 2.1).
2. The `patch` kind (`:1649-1700`): the readers-era proposal shape; the analyst writes side findings only (stop 21b). Keep for old proposals in the pool, or drop the pool's old runs.
3. `select_entry_rule` (`:2410-2423`), a mirror of the runner's `_select_entry`, pinned by a test; the runner passes its own.
4. `SECONDS_PER_BACKTEST`, `COST_BASIS_SOURCE`, `N_VARIANTS` (note 9): re-measure or drop the seconds figure from the record.
5. R1 and its tree (`:1228-1575`, `composition.py`, `_prepare_r1`/`_register_r1`/`_record_r1_failure` in `RC:5317-5452`): until a second block exists, a flag-on path nothing exercises outside tests; given the operator's remark, a candidate for `enabled: false` rather than deletion.

### (3) Disagreements between the speech and the element

1. Step 7, "The rest rank by the analyst's confidence score, then fewer backtests, then name": correct, with the consequence in note 2 unstated.
2. Step 3, "drawn at random among folds A to D the source run is not on": correct; the one-generation limit is not said (note 5).
3. Step 5: correct (`:1759-1768`). Step 6, "windows times 3 variants times coins": `N_VARIANTS` (`:134`), against four real variants (note 9).
4. Step 8's order (R1, scheduled, top candidate, R2, stop): `:2476-2548`; correct. Step 10: `:2646-2832` (read at stop 01); correct.
5. "Recorded cost basis: 10.2 seconds per backtest, 3 variants (`:134-139`)": verified; stale (note 9).
6. Section 6, "My grep found no code reader of the brief's source observations outside this tool and tests": consistent with stop 01 note 1.9.
7. Reading map verified: `decide_next.py:1-107`, `:128-215`, `:1612-1700`, `:1740-1800`, `:1876-1947`, `:2256-2332`, `:2334-2423`, `:2426-2580`, `:2587-2624`, `:2630-2643`, `:2646-2832` (stop 01); `novelty.py:186-208`, `:250-283`; `research_folds.py:272-318` (stop 06); `decision_record.schema.json:7`. Not opened: `:226-330`, `:332-537`, `:539-616`, `:617-641`, `:644-1022`, `:1173-1226`, `:1228-1575`, `:1949-2136`, `:2138-2254`; `composition.py`.

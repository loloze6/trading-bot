# Stop 09: The claim test (what a signal knows)

## Speech (verbatim)

**Stop 09 of 29: The claim test.** Open on the side: `tools/claim_tests.py`, `tools/claim_card.py`, `tools/claim_measure.py`, `tools/claim_findings.py`, `workflow_artifacts/skills/claim-revision/SKILL.md`, `run_phase1_research.py`, run_102's claim files.

**In one sentence.**
The claim test turns the idea's belief into one measurable sentence ("on these bars, what happens next differs from those other bars, measured like this") and measures it on the backtest's own bars, without ever grading it.

**Why it exists.**
A backtest says whether a strategy made money. It does not say whether the belief behind it is true.
A strategy can win for the wrong reason, or lose while its signal really does know something. The claim test measures the belief itself, so a later run can build on what was learned, not only on what was earned.
It is information only, on purpose: the real pass or fail stays with the grid (the pre-registered criteria), the profit bars and the holdout.

**What comes in, what goes out.**
- In: the claim block of the hypothesis card (written at step 1a, stop 07); the block manifest (which part of the config is the idea, from step 1b); the bars each backtest saved.
- Out: a check record before any spend; a match record after step 1b; a revision record; the measured effect sizes per variant and per run; a "finding" in campaign memory; two campaign-wide lists: claim coverage and test requests.
- Next: the analyst reads the findings (stop 21); decide-next carries a claim to the follow-up run on another fold, where it is measured again (fold confirmation, stop 19).

**What happens here, step by step.**
1. A test is built from four slots. Which bars (the selector: all bars, an event, a regime, a regime change, a calendar slice, a quantile). What happens next (the outcome: forward return, forward volatility, forward drawdown, trend ends). Compared with what (the baseline: the other bars, a shifted placebo, another selector). Measured how (the statistic: mean difference, rank correlation, hit rate, decay over horizons). A claim holds one to three tests, each with a direction and a minimum sample.
2. Selectors read only what is known at the bar's close (its forecast and price), never the future: the outcome is computed by code after.
3. Right after step 1a, code checks every claim: only the allowed slots, at most three tests, a reachable minimum sample given the bars and coins. A refused claim gets one retry of 1a; then the run goes on regardless (stop 07). A run that reaches step 1b without that check gets it once there, without a retry.
4. After step 1b, code compares the claim with the block the config built. If no test reads the block's own output (its forecast, or its regime label), the claim is "blind": it measures price, not the idea. An AI (the claim-revision skill) may then rewrite the tests once; statement and kind stay locked; a pre-filled claim is never revised.
5. After the backtests, every test is measured on each graded variant's saved bars: effect sizes and the sign window by window, per coin. Labelled "measured, not proven": no p-value, no verdict.
6. At the record-keeping step, the measurement becomes a finding in campaign memory, and one row in the findings summary.
7. A claim the slots cannot express is written as "no test" with the missing block named; it goes to the test-request list.

Example: run_102's claim was pre-filled from run_101 ("the slow trend leg carries the persistent part of the forecast"). Its one test selects the top fifth of 168-hour past returns. It reads price, not the forecast, so the match record says `block_visibility: blind`; being pre-filled, it was not revised (`claim_revision.yaml`: `status: frozen`). It was measured on all 4 variants (`claim_measurement.yaml`: `claim_status: measured`).

**What it costs and how long it takes.**
The checks and the measurement are code, no AI call. A claim revision would be one AI call; run_102 made none.
911 lines in `campaign_record/claim_test_coverage.yaml`, 80 in `test_requests.yaml`; 26 findings in run_102's `findings_summary.yaml`.

**What is switched off or not used here.**
- The verdict path is kept in code but parked: significance methods, the verdict rule, the calibration gate and the grading command are called by no run (decision D-077).
- Trade-level tests are accepted only with the analyst switch on; they are effect sizes only.
- Regime selectors give effect sizes only: no significance method exists for them.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Engine header | `tools/claim_tests.py:1-215` | Slots, definitions, no-lookahead note, parked verdict path |
| Signals and bars | `tools/claim_tests.py:217-555` | Forecast signals, window, bars reader, warm-up, graded variants |
| Selectors | `tools/claim_tests.py:559-734` | all, past return, volatility, forecast fields, event, regime, regime change, calendar, quantile, all_of |
| Outcomes | `tools/claim_tests.py:735-784` | forward return, volatility, drawdown, trend ends |
| Baselines | `tools/claim_tests.py:786-845` | complement, placebo, other selector |
| Statistics | `tools/claim_tests.py:846-912` | ranks, Spearman, mean diff, hit rate, rank IC |
| Test spec | `tools/claim_tests.py:913-1009`, `:1110` | `TestSpec`, `spec_hash`, `check_spec` |
| Trade tests | `tools/claim_tests.py:1250-1685` | Gated trade-level family |
| Claim check | `tools/claim_card.py:52-265` | Kinds, keys, `check_claim` (`:193`), max 3 tests |
| Block match | `tools/claim_card.py:347-465` | Columns read, `block_visibility`, `match_check` |
| Power | `tools/claim_card.py:468-552` | Bars per window, `power_warnings` |
| Coverage and requests | `tools/claim_card.py:554-665` | `record_coverage`, `append_test_requests`, summary lines |
| Measurement | `tools/claim_measure.py:49-407` | Labels, `measure_test` (`:188`), `measure_variant` (`:245`), `run_doc`, holdout refusal (`:122`) |
| Finding | `tools/claim_findings.py:296-386`, `:432` | `build_finding`, `findings_summary` (max 200 rows) |
| Revision skill | `skills/claim-revision/SKILL.md` (48 lines) | One rewrite of the tests; statement and kind locked |
| Check after 1a | `run_phase1_research.py:17737-17800` | Stop 07 |
| Check before 1b | `run_phase1_research.py:17865-17880` | Once, no retry |
| Match record | `run_phase1_research.py:17883` | `claim_match.yaml` |
| Revision after 1b | `run_phase1_research.py:18319-18341`; AI call `:17989` | `claim_revision.yaml` |
| Measured after backtests | `run_phase1_research.py:18437-18488`; called `:20648-20653` | `claim_measurement.yaml`, per-variant `claim_test.yaml` |
| Finding at regroup | `run_phase1_research.py:18653` | Into the memory entry |
| Records | `campaign_record/claim_test_coverage.yaml`, `campaign_record/test_requests.yaml` | Campaign-wide |
| Examples | `runs/run_102/artifacts/claim_match.yaml`, `claim_revision.yaml`, `claim_measurement.yaml`, `variants/base/claim_test.yaml`, `findings_summary.yaml` | blind, frozen, measured on 4 variants |

Remarks: send them as "stop 09: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Step 9: 

Here i find back concepts that i agree with. 
But i am lost now on this step compared to previous one (where design was challenged) 
Agree here on your stop explanation, the why and rationale. 
So i am concerned when you say "It is information only, on purpose. The real pass or fail stays with the grid (the pre-registered criteria), the profit bars and the holdout." because the pre-registered criteria creation design of step 8 is really challengeable, while the explanation of this stop is more amigned with my vision.

Also i do not get "The checks and the measurement are code, with no AI call". A claim test (defining criteria testing an ideas cannot be done by code, no?)

## Inspector notes

### (1) Design and mechanism

1. The engine is careful where it must be. Selectors read bar t only (`BAR_T_FIELDS :175-176`, `check_spec :1014-1016`), `past_return`/`trailing_vol` are undefined across windows and in the first n bars (`:564-603`), outcomes are timestamp-matched inside one window (`:318-328`, `:735-747`), the quantile is trailing (`:686-701`), the placebo shifts by more than the longest horizon (`:786-829`), warm-up rows stop at the window start and refuse the holdout store (`:446-469`), and the measurement refuses any bar at or after the holdout start (`claim_measure.py:122-128`). The no-lookahead note (`:59-87`) is matched by the code. The spec hash is canonical and stable across key order and float spelling (`:951-976`). This is the best-built element so far.
2. What the engine never does is say whether the belief held. The card's `pass_if`/`fail_if` are "predictions in words ... code never reads these two fields" (`CLAIM_TESTS.md:69-73`); the measurement writes numbers and the label "measured, not proven" (`claim_measure.py:55-59`, `:217-220`). run_102's own card says pass needs "the claimed sign in at least 4 of the windows at each horizon" (`hypothesis_card.yaml:138-141`); the base variant measured 5/6 at h=6 and 3/6 at h=24 (`variants/base/claim_test.yaml:59`, `:109`): by the card's own words the claim failed on fold B, and no file says so. The verdict path is parked by D-077 (`claim_tests.py:16-26`), so the one place the loop could learn "this belief was wrong" is left to whoever reads the numbers: the analyst (stop 21) and the operator. For an autonomous loop, a prediction written down and never compared with its outcome is a record, not a learning. Whether `fold_confirm.grade_test` (stop 19) does the comparison is the open question; here nothing does.
3. run_102 shows the blind-claim problem the revision mechanism was built for, and the mechanism was switched off for it. The test selects on `past_return` (price) and reads no forecast; `claim_match.yaml:11` says `blind`, the revision is `frozen` because the claim is pre-filled (D-100, `claim_revision.yaml:2-4`), and the measurement proves the blindness: `base` and `split_stretch_weight`, which differ only in the forecast, have identical effects to the last digit (`findings_summary.yaml:60-75`). So the child run measured the market effect of a 168-hour rise on fold B, not the block the brief said the claim was about (`PREFILLED_CLAIM.md:12-15`). The loop then did adapt one generation later: the run_102-2 candidate's test reads `signal: debug_info.components.stretch_from_short_sma.post_pipeline_value` (stop 01, the D-193 key). The adaptation came from the analyst, not from this element.
4. The claim statement is a paragraph; the test is a fragment. run_102's statement makes two assertions joined by "therefore" (`:109-115`): the market effect, and that the stretch leg "adds sign flips without a matching reversal edge". The one test measures the first; the second is never tested. The engine's own definition is one sentence of four slots (`claim_tests.py:4-8`); `statement` accepts any text (`claim_card.py:107-108`, non-empty). A claim whose text outruns its tests records as "measured" with the untested half riding along.
5. Over half the campaign's findings were never measured: `findings_summary.yaml:10-11` gives 12 measured, 14 not measured of 26; `test_requests.yaml` holds 6 rows, 4 from the deleted readers stage (`:2-54`) naming blocks the trade family has since added (run_095's request, `:68-80`, is now expressible with `entry_forecast` + `trade_net_return`, `CLAIM_TESTS_TRADE.md:25-27`, `:66-70`). Nothing closes a request when its block arrives, and nothing re-measures an old claim with a new block. The request list is append-only in both senses.
6. The parked verdict path is dead twice over. Parked by D-077, and inapplicable to the live configs: method B's null needs `variant_signal` to accept the config, which refuses anything but one component with identity transform and weight 1 whose class is in `SIGNALS` (`:481-520`), and `SIGNALS` holds Donchian and Keltner only (`:265-267`). run_102's base has two components with standardise/negate transforms (stop 07). If un-parked tomorrow, it could grade none of the last twenty runs' configs.
7. The power check is honest and weak: an upper bound `bars // h_max x coins` (`claim_card.py:507-546`), minus the quantile lookback per window (D-175). It catches an impossible floor, not an unlikely one; run_102's 17,520 bars against a floor of 100 (`claim_power.yaml:8`) is never close. Fine as a sanity check; not a power analysis.
8. Information-only is enforced consistently: every caller wraps in `try/except` and records (`RP:17794-17795`, `:17879-17880`, `:17921-17923`, `:18329-18330`, `:18447-18448`, `:18669-18673`). The cost is the one in note 2: nothing downstream in code reads the numbers to decide, so the whole element's output is prompt material for the analyst and a row for the operator.

### (2) Legacy or simplifiable (leads)

1. The parked verdict path in `claim_tests.py`: the SIGNIFICANCE/VERDICT/calibration docstring (`:98-129`), `SIGNIFICANCE_METHOD*`, `A851A_*`, `CALIBRATION_*` (`:184-204`), `SIGNALS`, `FORECAST_TOLERANCE`, `compute_signal`, `donchian_forecast`, `keltner_forecast` (`:229-272`), `read_warmup` (`:446-469`), `variant_signal` (`:481-520`), `WARMUP_BARS`, `BLOCK_BARS` (`:209-210`), `Window.warm`/`signal` (`:296-297`), the significance check in `_check_tail` (`:1173-1181`) and `TestSpec.alpha`/`significance` defaults (`:921-923`), plus `tools/claim_tests_calibration.py` and the grading CLI (`grade_claim_file`, `main`, not read). Kept "as code and kept tested" by D-077; a separate module or a deletion is the operator's call. `claim_card.py:22-24` still says "The claim is supported only if every test passes (claim_tests.combine)".
2. `EXERCISED_ON_REAL_RUNS` (`:162-167`): a slice-1 record of which blocks had run on real data; run_102 alone exercised `quantile`, `past_return` and `complement`. Stale documentation as a constant; nothing reads it (not checked).
3. The module header (`:34-38`) says the trade family is refused "unless the caller passes trade_tests=True, and nothing in the pipeline does yet"; `_claim_check_kw` passes it under the analyst flag (`RP:17469-17474`), and run_102's findings carry three `execution_behaviour` claims (`findings_summary.yaml:16`). Three comments in one file (`:34-38`, `:1195-1201`, `CLAIM_TESTS_EXECUTION.md:3`) describe the gate as closed.
4. `OLD_RUN_FILE` compatibility (`claim_measure.py:62-65`, `:78-87`): the pre-D-077 name `claim_status.yaml`, read only for older runs. Delete once no run before D-077 is read back (run_070 onward are in the coverage record).
5. The claim text is stored five times per run: the brief (`candidate.claim`), the card, `claim_prefill.yaml:prefilled`, `claim_revision.yaml:claim_after` (written whole even when `frozen`), and the finding's `statement`. Each is a copy by code; one reference and one copy would do.
6. `claim_test_coverage.yaml` (911 lines): per run, `measured.tests` and `measured.looks` are the same list twice when there was one attempt (`:11-60`); `looks` is the accumulating one (`claim_measure.py:383-394`). Drop `tests` or make it a count.
7. `test_requests.yaml` rows with `stage: specialist_readers` (`:3`, `:15`, `:34`, `:46`): a deleted stage's rows, two of them now expressible (note 1.5). Close or re-label.
8. The 1a/1b `match_check` warning `claim_kind_vs_block_kind` (`claim_card.py:455-460`) and `KIND_BLOCK` (`:68-72`): the kind table maps five of thirteen kinds; the other eight "say nothing". Whether any reader uses the warning beyond the printed line was not checked.

### (3) Disagreements between the speech and the element

1. Step 1 lists the selectors as "all bars, an event, a regime, a regime change, a calendar slice, a quantile": `all_of` (`:704-721`) is left out of the sentence; the reading map has it. Omission.
2. Step 3, "A refused claim gets one retry of 1a; then the run goes on regardless ... A run that reaches step 1b without that check gets it once there, without a retry": `RP:17765-17789`, `:17865-17880`; correct.
3. Step 4, "An AI (the claim-revision skill) may then rewrite the tests once; statement and kind stay locked; a pre-filled claim is never revised": `_CLAIM_LOCKED_KEYS :17956`, `claim_revision.yaml:2-4`; correct. Not stated: the revision call runs on the default model, Haiku (`RP:17990-17991`, "same model and options as every stage"), not on 1a's Sonnet.
4. Step 5, "every test is measured on each graded variant's saved bars: effect sizes and the sign window by window, per coin": `claim_measure.py:188-234`; correct; the per-era split (`:210`) is also written. The speech does not say that the card's own `pass_if` is never compared with the result (note 1.2).
5. Example: `block_visibility: blind` (`claim_match.yaml:11`), `status: frozen` (`claim_revision.yaml:2`), `claim_status: measured` on 4 variants (`claim_measurement.yaml:6`, `:9`); correct. The example does not say that two of the four variants measured identically (note 1.3).
6. Section 6, "Trade-level tests are accepted only with the analyst switch on": correct against `RP:17474`; the element's own header says the opposite (note 2.3). "Regime selectors give effect sizes only": `REGIME_REASON`, `claim_card.py:84`; correct.
7. Section 5 figures: 911 lines (coverage), 80 (test requests), 26 findings (`findings_summary.yaml:7`): correct. "Revision skill (48 lines)": the file has 49.
8. Reading map ranges verified: `claim_tests.py:1-215` (docstring `:1-130`, constants to `:214`), `:217-555`, `:559-734` (selectors end `:728`), `:735-784`, `:786-845`, `:846-912`, `:913-1009`, `:1110`, `:1250-1685` (read to `:1339`); `claim_card.py:52-265`, `:193`, `:347-465`, `:468-552`, `:554-665`; `claim_measure.py:49-407`, `:188`, `:245`, `:122`; `claim_findings.py:296-386`, `:432`; `RP:17737-17796` (the map says `:17800`), `:17865-17880`, `:17883`, `:18319-18341`, `:17989`, `:18437-18488`, `:20648-20653`, `:18653`; the five example files and the two records.

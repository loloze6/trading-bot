# Delivery review — delivery plan v26 vs roadmap v27 (2026-09-27)

Read-only review of everything delivered under `engineering/delivery_plan_v26.md`, checked
against the plan itself and the target design in `engineering/engineering_roadmap.html` (v27)
plus every recorded operator decision. Master at `e623531d`. Seven agents (4 Sonnet inventory,
2 Opus vision check, 1 Opus "everything on" walk-through) plus the orchestrator's own Linear
check; their raw reports sit next to this file. Findings marked **[verified]** were re-checked
by the orchestrator against the code; the rest are the agents' evidence, not re-verified.

## In plain words

- **The plan was built.** Of 101 plan items, 70 are delivered as written and 12 delivered
  differently because of a recorded operator decision. The rest are either waiting on real
  runs (none has ever been done with the new pipeline) or are gaps listed below.
- **The safety core is right.** The holdout is reachable only through the profit-bars stop
  plus the operator's unlock; an idea's status comes only from the grid; refine/pivot/
  escalate/kill, the circuit breaker and families cannot run; every tested variant is
  counted as a trial; composition uses past data only.
- **But the new pipeline has never run end to end, and it would not today.** With every new
  switch on, a real run crashes before its first backtest (section A). The test suite is
  green because the only near-end-to-end test replaces the part that breaks.
- **Five places drift from the vision** (section B). The two biggest: the "different coin"
  variant never actually changes the coin, and the five experts see only one variant's
  results and score "distance to profitable" the opposite way from the roadmap.

## Scorecard (agents' counts)

| Part | Rows | Delivered | By decision | Partial | Missing | Deviated | Needs real run |
|---|---|---|---|---|---|---|---|
| Slices 0–3 | 35 | 26 | 2 | 1 | 2 | 1 | 3 |
| Slices 4–5 | 28 | 20 | 3 | 2 | 0 | 1 | 2 |
| Slice 6 (+ promotion-block row) | 17 | 13 | 4 | 0 | 0 | 0 | 3 (run budgets) |
| Slices 7–8 + cross-cutting | 21 | 11 | 3 | 3 | 1 | 0 | 4 |
| **Total** | **101** | **70** | **12** | **6** | **3** | **2** | **12** |

(Slices 0–3 also has 1 row the agent left unscored.)

## A. Would break a real run — fix before any real run

| # | Finding | Evidence | Status |
|---|---|---|---|
| A1 | Under config-direct authoring the `backtest_specification` and `protocol_execution` handoffs still require `artifacts/validation_protocol.yaml`, which nothing writes in that flow; the data-gate handoff `backtest_spec_to_data_availability_gate.yaml` is created only by `_create_remaining_handoffs`, called only on the legacy branch. `ensure_files` raises before the stage runs. Every forecast-block run dies at 5a after stages 1a, 1b and 2 are paid for. | `run_phase1_research.py` ~L11966-11968, L12270; `workflow_artifacts/templates/handoffs/validation_to_backtest_specification.yaml:13`; repro `repro_handoffs.py` | **[verified]** (repro run by the orchestrator in a temp dir) |
| A2 | Even with A1 fixed: `run_tool_worker` always passes `--validation-protocol`, and `run_protocol.py` opens it only after the backtests, so each variant would spend its data then fail. | `run_phase1_research.py` ~L1479/1519; `tools/run_protocol.py` ~L2289 | agent (reading) |
| A3 | No trading-bot interpreter on this machine: `../venv/Scripts/python.exe` and `../.venv/bin/python` do not exist, so `_resolve_tbot_python` raises for every tool stage. (Environment, not code.) | `ls` | **[verified]** |
| A4 | Those exceptions escape `run_loop`/`process_once` with no try: the campaign process crashes with no classified pause, status stays `active`, every restart crashes at the same place. | `run_campaign.py` ~L2696, ~L3536 | agent |
| A5 | 3-variant floor vs exactly 3 produced: one validator violation, patch failure or data refine pauses the campaign as `variant_gate_insufficient` (misleading label); no cap of 4 either. | `run_phase1_research.py` ~L12319, ~L2043-2139 | agent |
| A6 | First-run setup: the queue has no ready entry; 8 of 13 `protocols/*.json` carry the unratified generic promotion block, so the D-3 guard raises after three LLM stages. The first run needs a new brief with `machine_constraints`, a pin to a safe protocol, and a menu-shaped pass rule or `criteria_from: hypothesis_generation`. | `tools/protocol_resolution.py` ~L96 | agent |
| A7 | `_era_id_for_timestamp` still compares a date string with `None` for the open-ended last era (`era_2026_h2_forward_recorded`): `TypeError` the first time a window reaches that era. Known since 2026-09-20, never ticketed. | `tools/run_protocol.py:1410-1411` | **[verified]** |
| A8 | Flag dependencies are checked only after LLM spend (variant_loop→config-direct, composition_runs→4 prerequisites, anti-adjacency gate→regroup_record); seven flag readers use plain `bool()`, so a quoted `"false"` turns a flag on. | A3 report §1 | agent |
| A9 | The only near-end-to-end test replaces `setup_run` with empty-input handoffs and turns the data gate off, so A1–A3 are invisible to the suite. | `tests/test_e060_s3b_composition_wiring.py` ~L920-1107 | agent |

## B. Drifts from the vision

| # | Finding | Evidence | Status |
|---|---|---|---|
| B1 | **The "different coin" variant cannot change the coin.** The strategy config has no symbol field (design guide §7a "PROPOSED, NOT BUILT"); all variants share the run's protocol, whose symbols are the coins traded; the skill's own "asset" example patches a regime-detector period. "Validated on every variant" has never meant a second coin. | `docs/STRATEGY_DESIGN_GUIDE.md:396`; `innovation-expansion/SKILL.md:251-256` | **[verified]** |
| B2 | **The five experts see only the base variant**, contrary to the operator decision of 2026-09-22 (E-033 S1: readers "must receive ALL variants"). `build_reports.py` has no variant handling; under the variant loop the base reports' trade/bar sections are also "unavailable" because variant backtests write under `variants/<id>/`. | `tools/build_reports.py` (0 hits for "variant", L201-215); `E-033/S1_FINDINGS.md:434-440` | **[verified]** |
| B3 | **"Distance to profitable" is scored the opposite way from card I.** Card I: 3 = fills a missing block type, low correlation to the registry; 0 = neighbour of something validated. Reader skills: 3 = metric within ~25% of a pass threshold. It is decide_next's 2nd rank key, so the loop favours tuning the last idea over new blocks. Readers cannot see the registry. | `engineering_roadmap.html` card I; `readers/profitability-reader/SKILL.md:172-177`; `decide_next.py` ~L1574-1580 | **[verified]** |
| B4 | **A crashed variant drops out of the grid.** The failed variant gets a failed trial row (good) and `continue`; the grid grades the survivors only, so an idea can be `validated` on 1–2 of 3 variants and registered as a block. | `run_phase1_research.py` ~L1525-1572, ~L1685 | **[verified]** |
| B5 | Every variant runs all the protocol's coins and the menu fixes `symbol_reducer: null`, so coins are pooled: a failing coin can hide behind a passing one ("one symbol per variant" not honoured). | A2 A–G report | agent |
| B6 | Stage agents are not closed-book. | CUL-336 | **fix in progress** |

## C. Gaps (not blocking, need a decision or a ticket)

| # | Finding | Evidence |
|---|---|---|
| C1 | The grid tie-break "a genuine FAIL beats an under-sample cell" is labelled OPERATOR-CONFIRMED in code, but its record says it was an overnight autonomous call awaiting Jeremy's confirmation. **[verified]** | `verdict_criteria_evaluator.py` ~L1640; `E-046b/S1_FINDINGS.md:365-369` |
| C2 | Unratified placeholders go live when the flags flip: `profitability_bars.yaml` (`ratified_by: null`) and the residual-IC thresholds (`ratified: false`); by decision ratification is manual, so they must be signed off before any stop is trusted. | A2/A3 reports |
| C3 | Cost criterion `realized_edge_to_cost_ratio > 0.3` lets gross edge cover only 30% of fees; card E wanted "survives 2× costs". | A2 A–G |
| C4 | Scale-free refusal not implemented (`scale_free` read only in tests); operator briefs keep their own pass rule with no menu check; the registration lint was never extended after slice 2. | A1 0–3 (2.4), A2 A–G |
| C5 | Criterion menu lacks IC, correlation and regime-conditional criteria; ideas are judged mostly on profit-type measures. | A2 A–G |
| C6 | Composite configs are written by code, not by step 1b, with no recorded decision; composites take coins from the pinned validating run; `target_instrument_set` is read by nothing. | A2 A–G |
| C7 | Reader patches are re-graded on the same windows that prompted them, and 1a picks criteria after seeing the evidence; only trial counting and the holdout guard against curve fit. | A2 H–N (inference) |
| C8 | Residual IC re-runs a composite backtest with no trial row (accepted default, E-060 guess 5); a campaign-review "reframe" brief is registered ahead of reader candidates, unscored (accepted default, 6c guess 6). Revisit both. | A2 H–N |
| C9 | Promotion-block retirement (§3) was deferred from 6c "to a separate ticket"; no ticket exists. | A1 slice 6; Linear |
| C10 | The grid's run budget (re-grade run_054/058/059) cannot be spent: their pre-registrations are not menu-shaped. | A1 0–3 (2.8) |
| C11 | Schemas `grid_evaluation`, `idea_status`, `variant_patches` were never added (the others were). | A1 4–5, 7–8 |
| C12 | Score provenance is on trust: `model_id` self-reported, `rubric_version` free text, no citation per score. | A2 H–N |
| C13 | Readers still receive the legacy promote/kill/refine label via `profitability.yaml`; `pass_rule_evaluation.yaml` still written from the base variant. | A2 A–G |

## D. Tidy

- **Linear** has not moved since 2026-09-20: every plan-v26 epic (E-056, E-057, E-046a/b, E-058, E-059, E-060, E-036) still `Backlog`; most slice tickets not linked to their epic; CUL-270's fix (PR #146) merged 2026-09-19 but the ticket is still `In Review`. [verified]
- **Stale docs:** RUNBOOK ~L410 "decide-next … does not exist yet"; USER_GUIDE ~L883 "idea_status not read by any routing"; campaign summary still prints "distinct failed hypothesis families" (`run_campaign.py` ~L1975); bars-file comment about a hard-coded 0.95 DSR threshold; the Gemini-key-at-import note; the RUNBOOK python path; `variant_loop` still "blocked on slice 4b".
- **Plan text never annotated** where decisions superseded it (verdict_interpreter bypassed, not deleted; validation stage kept in STAGE_CONFIGS for flag-off byte-identity).

## Verified clean (the parts that matter most)

Holdout only via the branch-3 stop + `holdout_decision.yaml`, backtest by hand; status only
from the grid; retired routing unreachable under the flags (69 tests); every tested variant
counted, failures included; composition weights, residual IC and block standardisation use
past data only; the 5b-ii mis-build fully reverted; slice 6 tests 546/546.

## Decisions needed from the operator

1. **C1** — confirm or change the grid tie-break (a genuine FAIL on any cell → refuted, even if another cell lacks data).
2. **B1** — how the "different coin" variant should work: add a coin field to the strategy config (design guide §7a), or give each variant its own protocol/coin set.
3. **B3** — adopt card I's rubric for "distance" (needs the readers to see the block registry), or keep "closeness to threshold" and change the card.
4. **B4 / B5** — should a crashed variant make the idea at best `inconclusive`? Should coins be graded separately (per-coin cells) instead of pooled?
5. **C2 / C3** — the profit-bar values, the residual-IC thresholds and the cost-criterion threshold, before any real run.

## What this means for the next steps

Phase B (free wiring test) and Phase C (real runs) are **blocked by section A**. Recommended
order for delivery plan v2: (1) section A fixes plus a real end-to-end wiring test that uses
the real `setup_run` (so A1-type breaks can never hide again); (2) section B, after the
operator's decisions; (3) operator ratification of the placeholders (C2/C3); (4) then the
two real runs; (5) section C/D as housekeeping alongside.

# Guided tour of strategy_designer_v2: itinerary (direction, 2026-11-06)

Checked against the branch `ccr-6624e33e-aakrpv`. Paths are relative to the repository root; `V2` = `strategy_designer_v2/`, `TB` = `trading-bot/`. The real run for examples is `V2/runs/real_01_daily_breadth_fold_a/003` (the operator's daily breadth brief on fold A, run through the engine-only loop). The guide re-reads every file before speaking; line numbers are not given here on purpose, the files are short.

## The two rules every stop is held against
1. The engine is the only reader of bars. Branch 1 and branch 3 are computed from the engine's outputs. No step reads the price cache on its own; no quick check beside the engine.
2. Forecasts are linear. A claim carries a continuous strength; the component emits it; the engine's standardise transform grades it. No on-off book.
These are the first lines of `V2/README.md`. The first version of v2 drifted from both and was cleaned on 2026-11-06; the history is in `V2/CHANGES.md` and `V2/STEPBACK.md`.

## The live path
brief → ideas (one model call) → for each claim and symbol: the engine on every window of the fold at two sizes → branch 1 from the engine's per-window bars → branch 3 from the engine's per-window metrics → the book summary → the analyst (one model call) → one next claim or none → the engine again → record.

## Stops
| # | Element | Files (the element itself) | Also in play |
|---|---|---|---|
| 00 | Orientation: the two rules, the spine, the history | `V2/README.md` (whole), `V2/CHANGES.md`, `V2/STEPBACK.md` (headings; the last three entries in full) | root `CLAUDE.md` hard rules; `guided_tour/_post_tour/overall_review.md` Level 0 and `session_analysis.md` for why v2 exists |
| 01 | The brief | `V2/briefs/real_01_daily_breadth_fold_a.md` (the operator's), one night brief, the four-line head rule in `V2/README.md` | `V2/run.py` `read_brief` (which lines are read) |
| 02 | The model call | `V2/steps/ask.py` (whole) | the closed-book options of v1 it mirrors: `strategy-research/workflow/run_phase1_research.py` around `_stage_agent_options` (read, not copied) |
| 03 | The ideas step | `V2/steps/ideas/PROMPT.md`, `V2/steps/ideas/CLAIM_FORMAT.md` (whole), `runs/.../003/claims.yaml` | the `already_tried` list from `V2/records/claims_tried.yaml` |
| 04 | A claim as code in the engine: the component and the grading | `TB/strategies/claim_linear.py` (whole); `TB/strategies/registry.py` (the `standardise` op and the transform registry); `TB/strategies/strategy_engine.py` (the three lines that write a component's debug fields; `forecast`) | `TB/tools/validate_config.py`; `V2/tries/try_09/READING.md` (what saturation and churn look like) |
| 05 | The engine step | `V2/steps/engine/backtest.py` (whole: `config_of`, `min_bars_of`, the two sizes, the refusals, `engine_verdict.yaml`); `TB/core/launcher.py` `run_backtest` (signature and docstring only) | one engine folder of run 003: `strategy_config_full_size.json`, `results/full_size/<window>/{bars.csv, metrics.json, trades.json}` |
| 06 | Branch 1: was the idea right? | `V2/steps/judge/judge.py` (whole); `judge_verdict.yaml` of one claim of run 003 | `V2/tries/try_10/READING.md` |
| 07 | Branch 3: is the book profitable? | the profit bar in `V2/steps/engine/backtest.py` (`_run_size`, the three checks, `passed_as`); `engine_verdict.yaml` of one claim of run 003; `TB/performance` metrics the bar reads (`core`, `bar_equity` blocks of `metrics.json`) | the sizing block (`TB/strategies/registry.py` `normalise_sizing_block`) |
| 08 | Branch 2: the analyst observes the book | `V2/steps/analyst/summarise.py` (whole), `V2/steps/analyst/PROMPT.md` (whole); `book_summary.yaml` and `analysis_r1.yaml` of run 003 | `V2/tries/try_11/READING.md` |
| 09 | The runner: the loop, resume, the knobs, the refusal | `V2/run.py` (whole) | `V2/tries/try_12/READING.md`; the `REFUSED` and `DONE` markers under `runs/` |
| 10 | The records | `V2/records/claims_tried.yaml` (shape and counts), `shelf.yaml` (the void note, `status`), `trials.yaml` (shape, counts by kind), `query.py` (whole) | who writes each: `run.py`, `backtest.py`, `judge.py` |
| 11 | What was tried and voided: the tries and the night | `V2/tries/*/READING.md` (01 to 12, in order), `V2/night_2026-11-06/README.md` and `ANALYSIS.md` | facts only: what each try showed, what the night's numbers were, why all of it is void |
| 12 | What is not built, and the operator's surface | `V2/README.md` "Status"; the open asks in `V2/night_2026-11-06/README.md`; `V2/STEPBACK.md` as the process; this itinerary | not built: the holdout path, a fold draw for children, a use for validated filters, replication as the engine on other coins, tests, speed of the engine |

## Setup choices
1. The inspector writes its own notes under "## Inspector notes" of each stop file; the guide never reads that section.
2. Stop files carry the three headings from the start; the guide fills Speech, then the operator's remarks verbatim.
3. Examples come from run 003 of the operator's brief; the guide opens no other run unless a remark asks.
4. Thirteen stops. v2 is small; each stop is one element, whole.

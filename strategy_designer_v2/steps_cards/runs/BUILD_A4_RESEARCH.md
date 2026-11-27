# Build A4, part 3: a research run in the new data use (2026-11-26)

Branch `build-a4-research`, from `80957b2`. Design: `common/data_use.md` (sections 1 to 4, 7), the operator's go of
2026-11-26. Build plan part 3: step 4's coins and windows, the explore and check halves.

## Purpose and expected outcome (written before the build)
- **Purpose:** a run started with `run_brief ... --data-use 2` is backtested on its 8 research coins over the 32
  research windows, step 7 explores only the windows before 2022, step 5 checks a confirm's direction on the windows
  from 2022; a run started without the flag runs exactly as before.
- **Expected:** (a) one fixed plan, steps 4 to 6 rerun on the base commit and on the branch: the same files, apart from
  run ids, times, the git commit and folder paths; (b) a small run end to end (`--data-use 2 --budget 3`): its
  `data_use.json`, every record on its 8 coins and 32 windows, the left-out windows counted, step 7's explorations on
  the explore half only; both test suites pass.

## What was built
| Where | What |
|---|---|
| `orchestration/run_brief/helper/run_brief.py` | `--data-use 2`: writes `orchestration/loop/<run>/data_use.json` once, `{"version": 2, "research_coins": coins.research_draw(<run>), "windows": "04_backtest/windows/research_2016.json"}`; kept as written when resumed; refused for a run that already tested ideas without it |
| `orchestration/run_idea/helper/run_idea.py` | **the one place that decides a run's backtest data:** when the run holds `data_use.json`, step 4 is called with `--data-use` on it |
| `04_backtest/helper/run_backtest.py` | `--data-use FILE`: the file's coins on its windows in place of the plan's coins and folds, one call per coin; a coin-window left out before the engine runs (data_use.md section 3), the window keeping its number; left-out windows counted per coin in `run.md` and on the index line; a copy of `data_use.json` in the record; data line `windows research_2016, data use 2` |
| `common/coins.py` | `data_use_file`, `new_data_use`, `data_use`; `dates`, `longest_hole`, `left_out` (the 90-day rule, then a hole of more than one day in the window, its edges included); `CHECK_FROM = 2022-01-01` |
| `common/lib.py` | `halves`, `check_windows`, `exploration_windows`: from the record's `data_use.json`, the explore half (`w1` to `w18`) and the check half (`w19` to `w32`); without it, the folds as before |
| `05_verification/helper/make_verdict.py` | the direction check on `check_windows`; in the new data use `direction_check` names `half` (`the check half (2022 onward)`) in place of `folds` |
| `07_common/helper/analyse.py` | explores `exploration_windows`; in the new data use the prompt says the later windows (the check half) are kept for the check, without the years |
| Cards | `common/explore_and_check.md` (a section for the new data use; the folds kept for old runs), `common/data_use.md` (part 3 built), `common/README.md`, the cards of `04_backtest`, `05_verification`, `07_common`, `run_brief`, `run_idea` |
| Tests | 7 new: the hole and 90-day rules (synthetic days, and XRP's real file: left out of its first 5 windows and of 2022-05, its 2-day hole), the run's `data_use.json`, `run_brief`'s writing and refusal, step 4 with `--data-use` (coins, kept numbers, counts, rerun kept), the halves against the folds, the index line's "ran" |

**A defect the run found, fixed:** step 4's index line said "not run" whenever every coin had at least one window not
run (the old rule read " not run" in each coin's summary). In this data use every coin's first windows after its listing
fail the engine's warm-up, so the run's first record said "not run" although 100 coin-windows ran. Now: "ran" when a
coin ran a window. In the old data use the line changes only for a record where every coin has a window not run; the
fixed plan below (4 coins with 24 of 24) is unchanged. The run's first record keeps the line written before the fix
(rerun in a scratch folder: "ran", proof (c)).

**Why this cannot leak:** the left-out rule reads a coin's daily file's dates only, never a price, and decides before
any bar is read; each window runs as before with its own warm-up; the halves remove windows from step 7's view and add a
check on windows step 5 already reads.

## Proofs
**(a) The default path is unchanged.** Plan `03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d1_own-range-close-height-fade_1d`,
steps 4 to 6 (step 5 with its stored `measure.py`, no model call), on the base commit (a worktree) and on the branch:
| | Files | Identical | Differ |
|---|---|---|---|
| All | 818 | 602 | 216 |
- Identical: every `bars.csv.gz`, `trades.json.gz`, `metrics.json`, `forecast_distribution.csv`, `trade_diagnostics`,
  the verdict's and the check's `result.json`, `size.json`, both `INDEX.md`.
- The 216 allowed differences: 141 `manifest.json` (run_id, created_utc, git_sha only), 36 `protocol_summary.json.gz` and
  36 `engine_log.txt` (run ids and temporary folder names), `run.md` (3 traceback lines: the checkout's path),
  `verdict.md` and `check.md` (the Plan and Record lines: the checkout's path). Results the same: confirmed (main
  0.00904, t 2.23, 378 cases), profitable enough, on both.

**(b) The new mode, end to end.** `run_brief 01_brief/briefs/060_falling-agitated-high-close-fades.md --run a4_research_run --data-use 2 --budget 3`:
- `orchestration/loop/a4_research_run/data_use.json`: version 2; coins **BCH, AVAX, ZEC, CRV, FIL, TAO, DOGE, ONDO**
  (one per category, the 8th ONDO); windows `04_backtest/windows/research_2016.json`.
- 4 turns, 3 ideas tested (060-01, 060-01.b1 by line 7.b, 060-01.b1.g1 by line 7.g, which first missed a component: the
  components step built `ScaledMoveSmallnessComponent`, see below), stopped on the budget: 3.80 of 3.00 USD (the idea
  started is finished). Step 4: 27.8 minutes in all.
- **Every record** (3 of 3): data line `BCH, AVAX, ZEC, CRV, FIL, TAO, DOGE, ONDO ...; 1d bars; windows research_2016,
  data use 2`, its `data_use.json` identical to the run's, 8 coins × 32 windows = 256 coin-windows:
  | Record | Run | Left out (first 90 days) | Left out (hole) | Not run by the engine |
  |---|---|---|---|---|
  | 060-01 | 100 | 126 | 0 | 30 |
  | 060-01.b1 | 100 | 126 | 0 | 30 |
  | 060-01.b1.g1 | 129 | 126 | 0 | 1 |
  Left out per coin: BCH 6, AVAX 19, ZEC 4, CRV 15, FIL 16, TAO 27, DOGE 13, ONDO 26. Not run: the engine's own
  warm-up rule, in the first windows after a coin's 91st day (the config needs 395 bars before a window: "strategy not
  ready after 131 warm-up bars", or the warm-up reaches days before the coin's file, "dates not fetched"). None of the 8
  coins has a hole of more than one day in the windows (XRP has one, in 2022-05: the test above).
- **The halves:** step 7 ran 6 analyses (7.b 3, 7.g 3), 10 explorations; the years in their outputs: 2017 to 2021 only,
  none from 2022. Step 5: 3 verdicts, all inconclusive, so no direction check ran in the run itself; the check half was
  proven on a real record instead (c).
- Steps 1 to 7 cost 3.55 USD (step 3 1.21, step 5 0.50, step 7 1.84) plus the components step 0.24.

**(c) On real records, outside the run (scratch folders, no model call).**
- The fixed plan of (a) in data use 2 (`--data-use` on the run's file): ran on the same 8 coins, same counts as 060-01
  (100 run, 126 left out, 30 not run), index line "ran"; step 5 with its stored measure: inconclusive (main 0.00415,
  t 0.77). Its check half, by step 5's own functions on this record: windows `w19` to `w32`, 14 of the record's 26
  windows with bars; the measure on them: +0.00375 (285 cases) against +0.00415 on every window: **agrees**; the
  verdict line reads "Direction check on the check half (2022 onward) ...: agrees: main measure +0.003752 on the check
  half (2022 onward) against +0.004146 on every window".
- Repeat: 060-01's step 4 rerun with the final code into a scratch folder: the same 770 files; 100 of 100
  `bars.csv.gz`, `trades.json.gz` and `metrics.json` identical; its index line "ran".

**Tests.** `pytest -q strategy_designer_v2/steps_cards`: 182 passed. `cd trading-bot && pytest -q`: 1678 passed, 16
skipped (a first run during the components step's build had 2 failures in `test_trailing_return_stds.py`: the build was
writing its candidate into `strategy_components.py` at that moment; rerun after the build: 0 failures).

## What this changes elsewhere, and what is left
- **Shared code:** this build changes nothing in `trading-bot/`. The run's components step added
  `ScaledMoveSmallnessComponent` to `trading-bot/strategies/strategy_components.py` (and its test, its build record
  `components/builds/ScaledMoveSmallnessComponent/`, the catalogue line), on this branch, under the standing go of
  2026-11-17; merging it into master stays the operator's go.
- **Not built (later parts):** the unseen test is still called by `run_idea` for a confirmed and paying idea in the new
  data use; its unseen dates (2016-17, 2026) overlap the research windows, so its "holds" means nothing there.
  `data_use.md` removes it and part 4 replaces it with step 9 (no idea of this run reached it).
- The plan's own header still names the brief's coins and folds; in the new data use the record's data line says what
  ran.
- One partial commit (`e30dd0a`) took in the run's files as they stood mid-run; this record's commit completes them.

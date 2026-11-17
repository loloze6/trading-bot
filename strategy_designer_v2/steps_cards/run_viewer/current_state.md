# The run viewer: current state (measured 2026-11-17 on branch ccr-6624e33e-aakrpv at 374eb5a48)

## The runs
A run is a `<name>_run` folder in a step's folder. 11 run names, measured:

| run | briefs | ideas (step 2 folder) | plans (step 3) | backtests (step 4) | step 5 results | step 6 results | step 7 results | run_idea table / loop queue |
|---|---|---|---|---|---|---|---|---|
| demo_run | 1 | 12 | 13 | 13 | 12 | 12 | 30 | yes / yes |
| night_run | 3 | 39 | 30 | 20 | 19 | 19 | 45 | yes / yes |
| night_005_run, night_006_run, night_012_run, night_rsi_run | 1 each | 2 to 8 | all refused | 0 | 0 | 0 | 0 | yes / yes |
| night_013_run | 1 | 33 | 34 | 20 | 19 | 19 | 42 | yes / yes |
| volume_run | 4 | 19 | 20 | 12 | 11 | 11 | 28 | yes / no |
| full_data_run, hourly_run, validation_run | 2 to 4 | 0 to 12 | 9 to 27 | 10 to 24 | 12 to 23 | 1 to 23 | 0 | no / no (steps called one by one) |

## Which file holds what
| what the operator wants to see | file (all committed) |
|---|---|
| the run's purpose, outcomes, reading | `steps_cards/<NAME>_RUN.md` (the six night runs share `NIGHT_RUN.md`) |
| the brief | `01_brief/<run>/briefs/<id>.md` |
| the ideas, and how they lead to one another | `02_ideation/<run>/ideas/<id>.md`; the id is the lineage: `011-01_x.b1_y` is the first idea line 7.b wrote from `011-01_x` |
| step 3: plan or refused, and why | `03_test_plan/<run>/plans/<backtest>.md`: front matter `outcome:` (plan, missing-components, untestable), `fit:`, and the `Reason:` paragraph |
| step 5: confirmed, inconclusive, rejected, with its t | `05_verification/<run>/verdicts/<backtest>/result.json`: `status`, `main_measure.statistic.value`, `decided_by` |
| step 6: profitable enough or not, the measures that failed | `06_profitability/<run>/checks/<backtest>/result.json`: `status`, `measures[]` with `passed`, `decided_by` |
| step 7: the lines and the ideas they proposed | `07<x>_<name>/<run>/<backtest>/result.json` (07a_not_observable ... 07g_patterns): `line`, `findings`, `ideas`, `idea_ids`, `no_ideas` |
| the order the loop took the ideas, and why | `orchestration/loop/<run>/loop.jsonl` (one line per turn) |
| the ideas waiting | `orchestration/loop/<run>/queue.json` (`status`, `score`) |
| cost and time | `orchestration/run_brief/<run>/journal.jsonl` and `orchestration/run_idea/<run>/journal.jsonl`: one line per step call, `usd`, `seconds`, `at` |
| the book, window by window | `04_backtest/<run>/backtests/<backtest>/<coin>/w<k>/metrics.json` (`core.net_return_pct`) and `manifest.json` (the window's last bar, to put windows in time order) |

`orchestration/run_idea/<run>/table.json` is a summary of the step files above; it exists for 8 runs of 11. The page reads
the step files directly, so the three runs without it show too.

## What is not committed
Per window, `bars.csv.gz` and `trades.json.gz` stay local (`04_backtest/.gitignore`), and none exist on this machine. They
hold the book's value bar by bar and the coins' closes. So, from what is committed:
- the book's value over time can be drawn **window by window** (24 points for 4 folds of 6 windows), not bar by bar;
- **holding the coins** cannot be drawn at all: no committed file holds the coins' return per window.

Proposal (needs the operator's go, a change to step 6): step 6 already computes, per window, the book's and holding's
equal-weight daily returns (`check_profitability.py::load`). It writes them as `curve.csv` beside its `result.json`:
one row per window, in time order: `window` (w1..), `book_return`, `hold_return`. 24 rows, under 1 KB per idea; it gives
the chart its second line and makes both lines the exact series step 6 measured. Variant: one row per week (about 420
rows, ~12 KB per idea) for drawdowns inside a window.

## The v1 viewer (`strategy-research/tools/run_viewer/`), what is kept
Kept: read-only, one JSON per view built from the files, phone width first, no network, dark mode.
Dropped: the server, the four levels, the raw-file views, the date masking module (this page shows no date: it shows
only text that is already in committed files, and labels the chart by year).

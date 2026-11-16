# Phase 1: where one idea's run spends its time (2026-11-16)

Source: the only recorded run, `demo_run` (4 ideas, run by `loop`). Read: `run_idea/demo_run/journal.jsonl`, the 576
window records in `04_backtest/demo_run/backtests/` (`manifest.json`, `engine_log.txt`, `run.md`). Not available: the
helpers' logs (`logs/` is git-ignored and was written on the machine that ran the loop). No model call was made.

## Per idea and per step (minutes of real time)

| Idea | Step 3 plan | Step 4 backtest | Step 5 verdict | Step 6 check | Step 7 lines | Real total | Table says |
|---|---|---|---|---|---|---|---|
| d1 (plan already existed) | 0 | **11.6** (86%) | 0.6 (5%) | 0.04 | 1.2 (9%) | 13.4 | 15.2 |
| e1 | 0.5 (4%) | **9.8** (78%) | 0.7 (6%) | 0.05 | 1.5 (12%) | 12.5 | 13.7 |
| e2 | 0.4 (3%) | **9.8** (81%) | 0.6 (5%) | 0.03 | 1.3 (10%) | 12.1 | 13.1 |
| g1 | 0.4 (4%) | **8.2** (78%) | 0.7 (6%) | 0.07 | 1.1 (11%) | 10.4 | 12.6 |
| **Average of e1, e2, g1** | 0.4 (4%) | **9.3 (79%)** | 0.7 (6%) | 0.05 | 1.3 (11%) | **11.7** | |

- Measured: every number above, from the journal (step start = its end time minus its seconds).
- Step 7 lines already run **at the same time**; their real time is the slowest line (60 to 90 s). The run table's
  "Minutes" adds the lines' times up, so it overstates an idea by 1 to 2 minutes.
- Steps 3, 5 and 7 are model calls: about 2.4 minutes per idea together. Step 4 (no model) is four fifths of the run.

## Inside step 4

Step 4 runs **144 backtests per idea, one after the other**: 6 coins x 24 windows (folds A to D), each window a new
Python process (`run_backtest.py` -> `run_protocol.py` -> the bot's `run_backtest`).

| Idea | Windows | Seconds per window (mean, min to max) | Per coin (24 windows) |
|---|---|---|---|
| d1 | 144 | 4.8 (4.1 to 6.1) | about 1.9 min |
| e1 | 144 | 4.0 (3.3 to 4.9) | about 1.6 min |
| e2 | 144 | 4.1 (3.6 to 5.1) | about 1.6 min |
| g1 | 144 (shorter windows: about 243 bars instead of 521) | 3.4 (3.0 to 3.9) | about 1.4 min |

Measured (gaps between the windows' `manifest.json` timestamps, written as each window ends):
- **No coin is slower than the others** (coin means within 0.3 s of each other).
- **No separate data-loading phase**: changing coin costs the same as a normal window.
- **Start and end of the step**: under 5 s, except e1 (about 14 s more before its first window; I do not know why).
- **Data did not change during the run**: the same coin and window range has the same data hash in all four ideas.
- g1's windows are half as long but only about 15% faster: most of a window's time does not depend on its length
  (estimate; g1's config also differs).

Inside one window: measured on this PC (4-core laptop; one window here takes 7.1 to 8.7 s, against about 4 s on the
machine that ran the loop). The re-run gave a `metrics.json` identical to the recorded one (120 of 120 fields).

| Part of one window | Share | How known |
|---|---|---|
| Starting Python and importing the bot (pandas, sklearn, hmmlearn, scipy, binance client) | about 1/3 (2.6 s here) | measured |
| Engine, bar by bar | about 22% | estimated (profiler) |
| Writing files | about 21%, of which about 3/4 are files step 4 then throws away (`portfolio_states.csv`, two Excel files) | estimated (profiler) |
| Warm-up (61 bars fed before the window) | about 14% | estimated (profiler) |
| Wrapper checks (holdout guard, summary) | about 5% | estimated (profiler) |
| Loading the coin's prices | about 3% | estimated (profiler) |

In short: an idea takes about 12 minutes; 9 of them are 144 small backtests run one by one, and a third of each is
Python starting up again.

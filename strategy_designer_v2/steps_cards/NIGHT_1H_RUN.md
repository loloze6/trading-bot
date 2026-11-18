# Night run on hourly bars (brief written 2026-11-18, before the run)

## Purpose
Do hourly bars give ideas that are real and pay after costs? The engine is now fast enough for hourly ideas (orchestration/duration/
8 and 9), step 4 runs any bar size, step 6 counts trades per day, and the gap rule ignores holes of up to one day on any
bar size (operator, 2026-11-18). Costs are the main enemy on hourly bars (15 to 25 bps a round trip): an idea must earn
more than that per trade.

## Three tracks, run at the same time (operator, 2026-11-18)
| Run | What | How |
|---|---|---|
| `retest_1h_run` | the 12 ideas confirmed and profitable on daily bars (UNSEEN_RUN.md), each unchanged but planned on 1h bars | `run_idea` on each, the idea's header set to `bar: 1h` (an operator's run decision, as `hourly_run` did); steps 3 to 7 and the unseen test as validated |
| `slow_1h_run` | a brief, from a theme: ideas read on hourly bars that trade rarely (positions held for days), so costs stay small | `run_brief --theme`, the brief's header `bar: 1h`, then its loop |
| `intraday_1h_run` | a brief, from a theme: effects within the day (time of day, moves within a day, short momentum or reversal) | `run_brief --theme`, `bar: 1h`, then its loop |

Default data: BTC, ETH, LTC, XMR, XRP, ZEC, folds A to D (24 windows), as every run. Budget: 200 USD in all
(operator, raised from 100: retest about 20, slow 90, intraday 90, each as its run's `--budget`). The three tracks run
at the same time (operator: parallel): model calls wait while backtests compute; the 4 cores are shared. Time is the
other limit: an hourly idea takes about 15 minutes to an hour alone (more with a long history), longer when shared.
Components: the loop calls the components step on its own; the operator also allows building one by hand when ideas
wait for it (the same step, its checks and proof).

## Expected outcomes, fixed now
**Retest (12 ideas):**
- **A. Most hold** (8 or more confirmed by step 5 AND profitable by step 6): the daily edge holds on hourly bars.
- **B. Confirmed, not profitable** (most confirmed, few profitable): hourly bars add trades and costs, not edge.
- **C. Not confirmed** (most inconclusive or rejected): the edge is a daily-scale effect; settings on hourly bars test
  another thing (an RSI of 14 hours is not one of 14 days).

**Slow and intraday briefs** (counts of ideas tested, confirmed, profitable): few profitable is the expected outcome on
hourly bars because of costs; the slow brief should do better than the intraday one. Any idea confirmed and profitable
gets the unseen test on 2016-17 (no hourly 2026 data yet: that period reads "not fetched").

## What is not done
No merge into master; no change to a step during the run; nothing is tuned to the night's results.

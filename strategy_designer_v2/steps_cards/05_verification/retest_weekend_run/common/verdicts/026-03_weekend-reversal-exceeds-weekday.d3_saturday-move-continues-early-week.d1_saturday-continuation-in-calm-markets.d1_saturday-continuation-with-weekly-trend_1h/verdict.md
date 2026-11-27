---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 48-bar return on entry forecast, pooled: 0.000912773; OLS slope t: 5.85936 (threshold: slope t >= 2 with >= 100 cases (and mean directional excess > 0) confirms; t <= -2 with >= 100 cases rejects)
- Supporting check: mean excess 48-bar return in forecast direction: 0.0066418, passed: True
- Counts: entry cases: 1472
- Decided by: Slope t is 2 or more with at least 100 cases and the mean directional excess return is above 0.
- Reading: The decision bar is taken as the bar read at Monday 00:00 UTC (closing at it, per the plan, or opening at it); the calm-market rule is taken from regime == 'trending' because the 8760-bar percentile cannot be rebuilt inside a window; Saturday/weekly signs use the recorded raw values, else recomputed from prices; each coin's mean 48-bar return uses non-overlapping grid stretches of all its windows; the slope t is the OLS t over all entry bars with a full 48-bar return.
- Size: unusual move +0.68 % (t 2.26, the cases of one day together: 364 days) per case over 48 bars, 0.101 of the coin's usual move (7.16 %); normal drift in its direction +0.03 %, total +0.71 %; 1408 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/common/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h`
Measure: `measure.py`

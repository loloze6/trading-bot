---
plan: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h
idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 18-bar excess forward return on forecast (grid cells): 0.00105331; OLS slope t: 7.89848 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: grid cells with forecast > 0: 5591, grid cells in total: 11111
- Decided by: The slope is positive with t >= 2: excess 3-day returns grow with the forecast's size.
- Reading: Situation bars are those with the recorded 180-bar return (recomputed from closes where missing) above 0 and a positive forecast; the coin's normal drift is the mean of its non-overlapping 18-bar grid returns over all its windows; all grid cells with a valid forward return and forecast enter the regression (forecast 0 included); the slope's t is the ordinary OLS t; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.54 % (t 2.27, the cases of one day together: 1820 days) per case over 18 bars, 0.055 of the coin's usual move (9.37 %); normal drift in its direction +0.71 %, total +1.25 %; 4716 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/common/backtests/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h`
Measure: `measure.py`

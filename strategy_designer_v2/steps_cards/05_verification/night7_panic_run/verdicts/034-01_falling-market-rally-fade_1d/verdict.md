---
plan: 034-01_falling-market-rally-fade_1d
idea: 034-01_falling-market-rally-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move after cases, short direction: 0.000147473; t of the mean, cases of one day summed: 0.0457231 (threshold: confirm: mean > 0 with t >= 2 (and slope t <= -2); reject: mean < 0 with t <= -2)
- Supporting check: slope of drift-adjusted 3-bar return on |post_pipeline_value| (t): 0.0745232, passed: False
- Counts: distinct case days: 726, cases: 1572
- Decided by: The main-measure t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The falling market is the 60-bar close change (in percent) below -10, recomputed from prices, falling back to the recorded regime ('unknown' = not vetoed) on a window's first 60 bars; an up day is a positive raw scaled return; the plan's 'fewer than 30 case days' is treated as a minimum count (not observable); the per-day t uses deviations from the mean summed per day (cluster standard error with D/(D-1)); the slope t is the ordinary OLS t.
- Size: unusual move +0.01 % (t 0.05, the cases of one day together: 726 days) per case over 3 bars, 0.003 of the coin's usual move (7.96 %); normal drift in its direction -0.36 %, total -0.35 %; 1572 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/034-01_falling-market-rally-fade_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/034-01_falling-market-rally-fade_1d`
Measure: `measure.py`

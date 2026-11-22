---
plan: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d
idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move after short bets (fall positive): 0.0022534; t of the mean: 0.779262 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on depth90 raw 90-day return (t = 2.942): 0.000500423, passed: True
- Counts: cases: 1045, coins with cases: 6, cases in regression: 1045
- Decided by: Inconclusive rule: the mean unusual move t lies between -2 and 2 (or is not positive at t >= 2) and no reject rule holds.
- Reading: A case is the first short bet (|forecast| rising >= 2 from its lowest level on the short side since the last bet, reset at flat or side change) in each 5-bar grid cell counted from each window's first row, cases whose 5-bar return would leave the window are dropped, the coins counted are those with at least one case, the slope t is the OLS slope over its standard error on cases with a recorded depth90 value, and too few cases gives 'not observable' as the workflow requires.
- Size: unusual move +0.23 % per case over 5 bars, 0.026 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.37 %; 1045 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d`
Measure: `measure.py`

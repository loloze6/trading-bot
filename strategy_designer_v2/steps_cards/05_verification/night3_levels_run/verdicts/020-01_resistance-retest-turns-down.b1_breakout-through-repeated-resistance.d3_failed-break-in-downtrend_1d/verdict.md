---
plan: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend_1d
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-removed 10-bar short-side move per short case: 0.00545669; t of the mean: 0.859091 (threshold: confirm: mean > 0 with t >= 2 over >= 20 cases and supporting check passes; reject: t <= -2 over >= 20 cases)
- Supporting check: larger minus smaller |forecast| half, mean short-side unusual move: -0.0267875, passed: False
- Counts: cases: 627, larger-forecast half: 313, smaller-forecast half: 314
- Decided by: t lies between -2 and 2 over at least 20 cases, meeting neither the confirm nor the reject rule.
- Reading: Cases are short bets (forecast rising by >= 2 points in size on the short side, per the workflow's case definition), the first per 10-bar grid cell of each window counted from its first row, with a full 10-bar return inside the window; drift is the mean 10-bar return on the same grid over all the coin's windows; the median split puts cases with |forecast| strictly above the median in the larger half.
- Size: unusual move +0.55 % per case over 10 bars, 0.043 of the coin's usual move (14.49 %); normal drift in its direction -1.17 %, total -0.63 %; 627 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend_1d`
Measure: `measure.py`

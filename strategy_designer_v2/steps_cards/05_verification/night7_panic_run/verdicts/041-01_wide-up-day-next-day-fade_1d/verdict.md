---
plan: 041-01_wide-up-day-next-day-fade_1d
idea: 041-01_wide-up-day-next-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move, next day, short direction: 0.00153978; t of the mean, cases of one day summed: 1.68947 (threshold: t >= 2 (with top third beating bottom third) confirms; t <= -2 rejects)
- Supporting check: top-third minus bottom-third mean unusual move by abs(forecast): -0.000656694, passed: False
- Counts: cases: 8849, distinct days: 2274
- Decided by: The t of the mean unusual move is between -2 and 2.
- Reading: The up-close situation is computed as close[t]/close[t-1]-1 > 0 inside each window, so active bars on a window's first row (no previous close) are left out of the agreement; cases are bars with a negative forecast and a next close in the same window, the drift is each coin's mean 1-bar return pooled over all its windows, the t clusters deviations by UTC day, the thirds are equal-size splits of the cases sorted by abs(forecast), and the plan's minimum counts lead to 'not observable'.
- Size: unusual move +0.24 % (t 2.25, the cases of one day together: 1942 days) per case over 1 bars, 0.053 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.12 %; 6076 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/041-01_wide-up-day-next-day-fade_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/041-01_wide-up-day-next-day-fade_1d`
Measure: `measure.py`

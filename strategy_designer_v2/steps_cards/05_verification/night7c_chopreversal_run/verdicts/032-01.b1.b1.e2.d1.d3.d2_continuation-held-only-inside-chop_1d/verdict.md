---
plan: 032-01.b1.b1.e2.d1.d3.d2_continuation-held-only-inside-chop_1d
idea: 032-01.b1.b1.e2.d1.d3.d2_continuation-held-only-inside-chop
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast/10, active bars: 0.00120581; OLS t, SE clustered by day: 1.56416 (threshold: t >= 2 with positive supporting mean confirms; t <= -2 rejects; at least 100 active bars)
- Supporting check: mean of sign(forecast) x next-day excess return: 0.00174208, passed: True
- Counts: active bars: 8058, days: 2546
- Decided by: The slope's t is between -2 and 2.
- Reading: Situation checked only on active bars with 30 prior bars inside the same window (earlier bars cannot be recomputed from prices and are left out of the agreement); the regression is OLS with an intercept and a standard error clustered by UTC day; fewer than 100 active bars is reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +0.14 % (t 1.26, the cases of one day together: 1764 days) per case over 1 bars, 0.030 of the coin's usual move (4.78 %); normal drift in its direction -0.01 %, total +0.14 %; 3640 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d3.d2_continuation-held-only-inside-chop_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d3.d2_continuation-held-only-inside-chop_1d`
Measure: `measure.py`

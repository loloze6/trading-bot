---
plan: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
idea: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
fit: adapted
status: inconclusive
---
Situation check: 93 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 84-bar excess return over the coin's drift per bet: 0.000537206; t of the mean: 0.0851178 (threshold: positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 to reject)
- Supporting check: OLS slope of excess return on forecast at signal bar: -0.000822625, passed: False
- Counts: non-overlapping cases: 1050
- Decided by: t between -2 and 2.
- Reading: a bet is a rise of the forecast of at least 2 points from its lowest positive level since the last bet (from 0 after a flat), the first bet in each 84-bar grid cell of a window counted from its first row is the case, and the drift is each coin's mean 84-bar return on that grid over all its windows.
- Size: unusual move +0.05 % per case over 84 bars, -0.008 of the coin's usual move (17.66 %); normal drift in its direction +2.09 %, total +2.14 %; 1050 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h`
Measure: `measure.py`

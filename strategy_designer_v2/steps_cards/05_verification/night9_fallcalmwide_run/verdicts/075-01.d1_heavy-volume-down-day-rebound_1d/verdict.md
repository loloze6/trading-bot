---
plan: 075-01.d1_heavy-volume-down-day-rebound_1d
idea: 075-01.d1_heavy-volume-down-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast, case days summed: 0.000739396; OLS slope t: 5.80686 (threshold: slope t >= 2 (with mean excess > 0) confirms; slope t <= -2 rejects)
- Supporting check: mean excess next-day return over case bars > 0: 0.00392222, passed: True
- Counts: distinct case days: 1676, case bars: 6801
- Decided by: The slope's t is 2 or more and the mean excess next-day return over the cases is above 0.
- Reading: Situation recomputed as close[t]/close[t-1]-1 < 0 and volume / mean of the 20 prior volumes > 1 (recorded heavy_vol raw value + 1 where present), active bars without a computable situation (first bars of a window) left out; cases with the same UTC day are summed (both excess return and forecast) into one observation for an OLS slope t; the plan's 300-day minimum, if not reached, gives 'not observable'.
- Size: unusual move +0.28 % (t 1.54, the cases of one day together: 1402 days) per case over 1 bars, 0.056 of the coin's usual move (5.31 %); normal drift in its direction +0.15 %, total +0.43 %; 4909 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0005981 on the check folds against +0.0007394 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/075-01.d1_heavy-volume-down-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.d1_heavy-volume-down-day-rebound_1d`
Measure: `measure.py`

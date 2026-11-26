---
plan: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d
idea: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward return minus coin mean 10-bar return on forecast (non-overlapping grid, non-zero forecast, pooled): 0.00151386; t of slope (day-clustered): 2.04668 (threshold: confirm: slope > 0 with t >= 2 and supporting check passed; reject: slope < 0 with t <= -2)
- Supporting check: mean directional excess return, top third of |forecast| minus bottom third: 0.0220602, passed: True
- Counts: non-overlapping grid cases with a non-zero forecast: 552, days: 143
- Decided by: The slope is positive with t >= 2 and the top third of |forecast| earns more in its direction than the bottom third.
- Reading: The situation is the regime column equal to the profile regime 'unknown' (rising calm, not vetoed) with the forecast's sign equal to the sign of the raw range position; the slope is an OLS fit with intercept and a day-clustered standard error (G/(G-1) correction); the coin's mean 10-bar return is taken on the non-overlapping grid of all its windows; thirds of |forecast| are equal-count splits of the cases sorted by |forecast|; the plan's minimum of 100 cases, if not reached, gives 'not observable'.
- Size: unusual move +1.01 % (t 1.43, the cases of one day together: 481 days) per case over 10 bars, 0.063 of the coin's usual move (15.92 %); normal drift in its direction +0.49 %, total +1.50 %; 832 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0006276 on the check folds against +0.001514 on every fold
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d`
Measure: `measure.py`

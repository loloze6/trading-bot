---
plan: 061-01.g1.d1.g1_day-move-follow-through-both-sides_1d
idea: 061-01.g1.d1.g1_day-move-follow-through-both-sides
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar return on forecast (non-overlapping grid): 0.000349244; OLS slope t: 2.03273 (threshold: slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject; over at least 300 cases)
- Supporting check: mean sign(forecast) x excess 5-bar return in top fifth of |forecast|: 0.00509723, passed: True
- Counts: grid cases: 3419, top-fifth cases: 684
- Decided by: Confirmed on every fold, but the main measure points the other way on the check folds (A, D), the years step 7 does not explore: main measure -8.497e-05 on the check folds against +0.0003492 on every fold.
- Reading: All grid bars with a 5-bar forward return inside the window are cases (all coins pooled, forecast 0 included), the coin's mean is over its grid returns in all windows, the top fifth is |forecast| at or above its 80th percentile, and fewer than 300 cases is reported as not observable.
- Size: unusual move +0.22 % (t 0.76, the cases of one day together: 1177 days) per case over 5 bars, 0.018 of the coin's usual move (10.60 %); normal drift in its direction -0.01 %, total +0.21 %; 3396 cases
- Direction check on folds A, D (the years step 7 does not explore): disagrees: main measure -8.497e-05 on the check folds against +0.0003492 on every fold
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.g1_day-move-follow-through-both-sides_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.g1_day-move-follow-through-both-sides_1d`
Measure: `measure.py`

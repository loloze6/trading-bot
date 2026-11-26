---
plan: 060-02.d1.d3_shrinkage-short-in-moderate-falls_1d
idea: 060-02.d1.d3_shrinkage-short-in-moderate-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (5-bar forward return minus coin mean 5-bar return) x forecast/10 on grid bars with forecast < 0: 0.0170544; t of the mean: 2.62318 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess 5-bar return, shrink bars minus growth bars, inside the regime (must be < 0): -0.0270727, passed: True
- Counts: active grid cases: 386, regime shrink grid bars: 386, regime growth grid bars: 213
- Decided by: Confirmed on every fold, but the main measure points the other way on the check folds (A, D), the years step 7 does not explore: main measure -0.0009326 on the check folds against +0.01705 on every fold.
- Reading: Situation taken as 20-day return in [-20 %, 0 %), 60-day return below -10 % (the falling profile of the config's veto) and a negative raw log volume ratio, short side, using the recorded regime where a window lacks the price history; 'inside the regime' read as bars whose recorded regime is 'trending', and the coin's mean 5-bar return taken on the same non-overlapping grid over all its windows.
- Size: unusual move +1.12 % (t 2.03, the cases of one day together: 348 days) per case over 5 bars, 0.102 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.53 %; 459 cases
- Direction check on folds A, D (the years step 7 does not explore): disagrees: main measure -0.0009326 on the check folds against +0.01705 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d1.d3_shrinkage-short-in-moderate-falls_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d3_shrinkage-short-in-moderate-falls_1d`
Measure: `measure.py`

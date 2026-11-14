---
plan: 002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum_1d
idea: 002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar forward excess return over coin mean, active grid bars: 0.028029; t of the mean: 0.968854 (threshold: mean excess > 0 with t >= 2 (and top-half minus bottom-half > 0) to confirm; mean excess < 0 with t <= -2 to reject; at least 30 cases)
- Supporting check: mean excess top half minus bottom half by forecast (median split): 0.022702, passed: True
- Counts: active grid cases: 205, top half cases: 102, bottom half cases: 103
- Decided by: t lies strictly between -2 and 2, which the plan calls inconclusive.
- Reading: Situation read from regime == 'trending' with forecast > 0; grid at positions 0, 20, 40, ... of each window with only bars having a full 20-bar forward return inside the window; the coin's mean 20-bar return is the mean over all its grid bars in all windows; the median split puts forecasts above the median in the top half and those at or below it in the bottom half.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum_1d`
Measure: `measure.py`

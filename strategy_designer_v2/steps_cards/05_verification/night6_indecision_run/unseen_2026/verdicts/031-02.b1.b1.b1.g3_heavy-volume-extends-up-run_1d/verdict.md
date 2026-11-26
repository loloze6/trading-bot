---
plan: 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d
idea: 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 3-bar excess return on forecast, trending grid bars: 0.000702956; slope t, cases of one day summed (day-clustered): 0.742873 (threshold: slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject)
- Supporting check: mean excess 3-bar return, forecast > 0 minus forecast = 0: 0.00382209, passed: True
- Counts: regime grid cases: 882, regime grid cases with forecast > 0: 424, regime grid cases with forecast = 0: 458, days: 97
- Decided by: The slope's t is between -2 and 2.
- Reading: The 6-day rise is recomputed as close[t]/close[t-6]-1 > 0 inside each window (the recorded regime is used only for a window's first 6 bars), the long side is forecast > 0; the regime grid cases are rows with regime == 'trending' at positions 0,3,6,... of each window with a 3-bar forward return in the window, the coin's mean 3-bar return is taken over all grid bars of all its windows, and the slope's t uses OLS with standard errors clustered by UTC day (residual-score sums per day, G/(G-1) correction).
- Size: unusual move +0.73 % (t 1.02, the cases of one day together: 203 days) per case over 3 bars, 0.086 of the coin's usual move (6.81 %); normal drift in its direction +0.03 %, total +0.76 %; 603 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d`
Measure: `measure.py`

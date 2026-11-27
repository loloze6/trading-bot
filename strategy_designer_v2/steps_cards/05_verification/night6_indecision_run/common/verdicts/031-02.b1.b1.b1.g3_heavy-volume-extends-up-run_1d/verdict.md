---
plan: 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d
idea: 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 3-bar excess return on forecast, trending grid bars: 0.000969574; slope t, cases of one day summed (day-clustered): 3.25875 (threshold: slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject)
- Supporting check: mean excess 3-bar return, forecast > 0 minus forecast = 0: 0.0125517, passed: True
- Counts: regime grid cases: 9058, regime grid cases with forecast > 0: 3975, regime grid cases with forecast = 0: 5083, days: 1172
- Decided by: The slope is positive with t >= 2 and the heavy-minus-light excess difference is above 0.
- Reading: The 6-day rise is recomputed as close[t]/close[t-6]-1 > 0 inside each window (the recorded regime is used only for a window's first 6 bars), the long side is forecast > 0; the regime grid cases are rows with regime == 'trending' at positions 0,3,6,... of each window with a 3-bar forward return in the window, the coin's mean 3-bar return is taken over all grid bars of all its windows, and the slope's t uses OLS with standard errors clustered by UTC day (residual-score sums per day, G/(G-1) correction).
- Size: unusual move +0.62 % (t 2.64, the cases of one day together: 1926 days) per case over 3 bars, 0.062 of the coin's usual move (9.27 %); normal drift in its direction +0.46 %, total +1.08 %; 5435 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d`
Measure: `measure.py`

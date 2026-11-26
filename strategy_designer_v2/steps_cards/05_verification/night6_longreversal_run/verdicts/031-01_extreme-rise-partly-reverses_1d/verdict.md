---
plan: 031-01_extreme-rise-partly-reverses_1d
idea: 031-01_extreme-rise-partly-reverses
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 30-bar unusual move in the short direction (return minus coin's normal 30-bar drift): -0.0427264; t of the mean, cases of one day taken together: -1.01624 (threshold: confirm: mean > 0 with t >= 2.0; reject: mean < 0 with t <= -2.0; at least 30 cases on at least 20 distinct days)
- Supporting check: none
- Counts: cases: 146, distinct days: 111
- Decided by: Inconclusive rule: t -1.02 lies between -2.0 and 2.0 (mean -0.0427) over 146 cases on 111 days.
- Reading: The situation is read from the recorded raw z90 (overreach last_history_value) >= 1 with a short forecast, a bar without that recorded value counting as outside the situation since 365-day volatility cannot be rebuilt from the windows' prices; a case is the first bet bar (forecast rising on the short side by >= 2 points from its lowest level since the last bet) in regime mean_reversion in each 30-bar grid cell counted from each window's first row, cases without a 30-bar return inside the window are left out, the normal drift is the coin's mean 30-bar return on the same grid over all its windows, the t is day-clustered (deviations summed per UTC day, with a G/(G-1) correction), and unmet minimum counts give 'not observable'.
- Size: unusual move -4.27 % (t -1.02, the cases of one day together: 111 days) per case over 30 bars, -0.134 of the coin's usual move (25.51 %); normal drift in its direction -3.86 %, total -8.13 %; 146 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-01_extreme-rise-partly-reverses_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-01_extreme-rise-partly-reverses_1d`
Measure: `measure.py`

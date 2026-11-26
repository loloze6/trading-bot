---
plan: 060-02.d2.d3_dry-up-in-moderate-declines_1d
idea: 060-02.d2.d3_dry-up-in-moderate-declines
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean sign-flipped 5-bar excess return on short-signal grid bars: 0.0131032; t of the mean, cases of one day summed: 1.76172 (threshold: mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects)
- Supporting check: OLS slope of sign-flipped excess return on |forecast|: 0.000619382, passed: True
- Counts: independent cases (days): 202, cases: 479
- Decided by: The main t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is the 10-bar return below 0 and the 60-bar return below -10 % (the profile veto), both from closes inside the window, with the recorded regime 'trending' standing in for the part that cannot be computed on a window's first 60 bars; the main mean is over the cases, its t uses the deviations summed per day (cluster standard error), the drift is the coin's mean 5-bar return on the same grid over all its windows, and 'fewer than 30 days' is reported as not observable.
- Size: unusual move +1.72 % (t 3.27, the cases of one day together: 351 days) per case over 5 bars, 0.154 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +1.13 %; 464 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d2.d3_dry-up-in-moderate-declines_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d2.d3_dry-up-in-moderate-declines_1d`
Measure: `measure.py`

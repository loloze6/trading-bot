---
plan: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d
idea: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move per bet (return minus coin's mean 3-bar return): 0.00803582; t of the mean, cases clustered by day: 0.913715 (threshold: confirm: mean > 0 with t >= 2 (and slope check passes); reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on signal-bar forecast (t): 1.43752, passed: False
- Counts: cases: 357, distinct days: 138
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Bets are rises of the long forecast of at least 2 points from its lowest level since the last bet (reset at flat), each 3-bar grid cell counted once at its first bet on a 'trending' bar, the move taken from that bar's close over the next 3 bars inside the window; the coin's mean 3-bar return is over its non-overlapping grid of all windows; the main t clusters deviations by UTC day; the slope t is the ordinary OLS t; active bars whose 20-day return cannot be computed inside the window (195) are left out of the situation check; the plan's 'fewer than 30 cases or 30 days' rule is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.80 % (t 0.92, the cases of one day together: 138 days) per case over 3 bars, 0.088 of the coin's usual move (6.81 %); normal drift in its direction +0.11 %, total +0.91 %; 357 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d`
Measure: `measure.py`

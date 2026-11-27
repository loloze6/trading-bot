---
plan: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d
idea: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move per bet (return minus coin's mean 3-bar return): 0.0132587; t of the mean, cases clustered by day: 4.03178 (threshold: confirm: mean > 0 with t >= 2 (and slope check passes); reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on signal-bar forecast (t): 4.42818, passed: True
- Counts: cases: 3409, distinct days: 1339
- Decided by: The mean unusual move is positive with t >= 2 and the supporting slope is positive with t >= 2.
- Reading: Bets are rises of the long forecast of at least 2 points from its lowest level since the last bet (reset at flat), each 3-bar grid cell counted once at its first bet on a 'trending' bar, the move taken from that bar's close over the next 3 bars inside the window; the coin's mean 3-bar return is over its non-overlapping grid of all windows; the main t clusters deviations by UTC day; the slope t is the ordinary OLS t; active bars whose 20-day return cannot be computed inside the window (1202) are left out of the situation check; the plan's 'fewer than 30 cases or 30 days' rule is reported as 'not observable' as the workflow requires.
- Size: unusual move +1.33 % (t 4.03, the cases of one day together: 1339 days) per case over 3 bars, 0.131 of the coin's usual move (9.27 %); normal drift in its direction +0.48 %, total +1.80 %; 3409 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d`
Measure: `measure.py`

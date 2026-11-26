---
plan: 031-01.g1_wide-day-low-close-rebounds_1d
idea: 031-01.g1_wide-day-low-close-rebounds
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return on forecast > 0 bars: 0.01307; t of the mean, cases of one day summed: 3.59307 (threshold: mean > 0 with day-clustered t >= 2 confirms (with slope > 0); mean < 0 with t <= -2 rejects)
- Supporting check: OLS slope of excess next-day return on forecast: 0.0176112, passed: True
- Counts: cases: 611, distinct case days: 305
- Decided by: The mean excess next-day return is positive with t >= 2 and the slope is positive.
- Reading: The situation is recomputed from prices inside each window (20-bar mean range including the current bar); every bar with forecast > 0 is a case on the 1-bar grid; the coin's mean is over all its 1-day returns in all windows; the t clusters deviations per UTC day with a D/(D-1) correction; the plan's 'fewer than 30 distinct case days' is applied as the minimum count (not observable).
- Size: unusual move +1.28 % (t 3.49, the cases of one day together: 302 days) per case over 1 bars, 0.256 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +1.40 %; 593 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.g1_wide-day-low-close-rebounds_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.g1_wide-day-low-close-rebounds_1d`
Measure: `measure.py`

---
plan: 032-02.b1_choppy-downside-break-one-day-rebound_1d
idea: 032-02.b1_choppy-downside-break-one-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move (return minus coin's mean daily return) over bars with forecast > 0: 0.0118898; t of the mean, cases of one day together: 1.97942 (threshold: confirm: mean > 0 with t >= 2.0 and slope > 0; reject: mean < 0 with t <= -2.0; else inconclusive; fewer than 30 distinct days: inconclusive)
- Supporting check: OLS slope of next-day unusual move on forecast: 0.00399139, passed: True
- Counts: cases: 124, distinct days: 94
- Decided by: The t lies between -2.0 and 2.0 (or cannot be computed), which the plan calls inconclusive.
- Reading: The situation is checked as close < min(low of prior 20 bars) (raw depth value < 0, recomputed from prices where not recorded) on the long side, without re-testing the choppy profile the code adds; the next-day return of a window's last bar is left out; the day-clustered t sums the cases' deviations per UTC day with a D/(D-1) correction; the plan's own 'fewer than 30 distinct days' rule is treated as the minimum count and reported as not observable.
- Size: unusual move +1.35 % (t 1.26, the cases of one day together: 36 days) per case over 1 bars, 0.232 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +1.46 %; 50 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/032-02.b1_choppy-downside-break-one-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-02.b1_choppy-downside-break-one-day-rebound_1d`
Measure: `measure.py`

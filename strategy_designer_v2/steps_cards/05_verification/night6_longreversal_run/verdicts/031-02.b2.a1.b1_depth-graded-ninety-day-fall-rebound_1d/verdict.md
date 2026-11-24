---
plan: 031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound_1d
idea: 031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 30-day return after positive-forecast mean_reversion cases (minus the coin's mean 30-day return): -0.0071343; t of the mean, cases of one day taken together (day-clustered): -0.197861 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; else inconclusive; at least 30 independent case-days)
- Supporting check: mean excess return of larger-forecast half minus smaller-forecast half > 0: 0.00182302, passed: True
- Counts: independent case-days: 35, cases: 85
- Decided by: The day-clustered t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are grid bars (positions 0, 30, 60, ... of each window with a full 30 bars ahead) whose regime is mean_reversion and forecast > 0; the coin's mean 30-day return is taken on the same grid over all its windows; the t sums the cases' deviations per UTC day with a G/(G-1) correction; with an odd number of cases the middle-forecast case is left out of both halves.
- Size: unusual move +3.84 % (t 1.10, the cases of one day together: 99 days) per case over 30 bars, 0.101 of the coin's usual move (26.78 %); normal drift in its direction +4.60 %, total +8.44 %; 153 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound_1d`
Measure: `measure.py`

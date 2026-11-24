---
plan: 031-02.b2.a1_deep-fall-rebound-nineteen-coins_1d
idea: 031-02.b2.a1_deep-fall-rebound-nineteen-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 30-bar forward return minus the coin's normal 30-bar drift, over grid bars with forecast > 0: -0.0071343; t of the mean, cases of one day taken together: -0.197861 (threshold: confirm: mean > 0 with t >= 2 and the check's difference > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual return of the larger-forecast half minus the smaller-forecast half: 0.0233915, passed: True
- Counts: cases: 85, distinct case days: 35
- Decided by: The main mean's t is between -2 and 2 (or undefined), meeting neither the confirm nor the reject rule.
- Reading: Cases are grid bars (positions 0, 30, 60, ... of each window) with forecast > 0 and a close 30 bars later in the same window; the normal drift is the mean of the coin's 30-bar grid returns over all its windows; the day-clustered t sums deviations per calendar day with a D/(D-1) correction; the halves are the top and bottom n//2 cases by forecast (the middle case left out when n is odd); fewer than 30 case days is reported as 'not observable' as the plan's minimum count.
- Size: unusual move +4.37 % (t 1.32, the cases of one day together: 107 days) per case over 30 bars, 0.114 of the coin's usual move (26.78 %); normal drift in its direction +4.56 %, total +8.93 %; 171 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b2.a1_deep-fall-rebound-nineteen-coins_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b2.a1_deep-fall-rebound-nineteen-coins_1d`
Measure: `measure.py`

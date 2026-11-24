---
plan: 031-02.g1_extreme-down-day-next-day-bounce_1d
idea: 031-02.g1_extreme-down-day-next-day-bounce
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return on bars with forecast > 0 (vs coin's all-window mean daily return): 0.00687924; t of the mean, cases of one day summed: 1.30228 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 100 independent case-days)
- Supporting check: forecast-weighted mean excess >= unweighted mean: 0.00781978, passed: True
- Counts: independent case-days: 200, cases: 492
- Decided by: t between -2 and 2.
- Reading: situation recomputed from the closes (20-day std with or without the current bar accepted, regime fallback at window starts); the coin's mean daily return is over all its windows' next-day returns; the t uses day-clustered deviations from the mean (deviations summed per UTC day, D/(D-1) correction) and the 100 minimum is read on distinct UTC days with a case
- Size: unusual move +0.47 % (t 0.91, the cases of one day together: 194 days) per case over 1 bars, 0.101 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.59 %; 459 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.g1_extreme-down-day-next-day-bounce_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.g1_extreme-down-day-next-day-bounce_1d`
Measure: `measure.py`

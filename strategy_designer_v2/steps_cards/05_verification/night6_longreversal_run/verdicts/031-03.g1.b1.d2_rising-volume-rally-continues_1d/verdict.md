---
plan: 031-03.g1.b1.d2_rising-volume-rally-continues_1d
idea: 031-03.g1.b1.d2_rising-volume-rally-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 14-bar excess return over the coin's mean, cases forecast > 0: 0.0400087; day-clustered t of the weighted mean: 1.70634 (threshold: confirm: mean > 0 with day-clustered t >= 2 and check passes; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: mean excess upper-half minus lower-half forecast (median split): 0.0355516, passed: True
- Counts: distinct case days: 141, cases: 655
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The 14-day return is recomputed as close[t]/close[t-14]-1 inside each window and the swell as the recorded raw vol_swell > 0, active bars whose first 14 rows cannot be evaluated are left out of the agreement; the coin's mean 14-bar return is the mean over all its windows' non-overlapping grid returns; the t clusters weighted deviations by UTC day with a G/(G-1) correction; the median split puts cases above the median forecast in the upper half and the rest (at or below) in the lower half, comparing plain means; the plan's 30-case-day minimum is applied as 'not observable'.
- Size: unusual move +2.46 % (t 2.45, the cases of one day together: 665 days) per case over 14 bars, 0.099 of the coin's usual move (20.98 %); normal drift in its direction +2.51 %, total +4.97 %; 1091 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2_rising-volume-rally-continues_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2_rising-volume-rally-continues_1d`
Measure: `measure.py`

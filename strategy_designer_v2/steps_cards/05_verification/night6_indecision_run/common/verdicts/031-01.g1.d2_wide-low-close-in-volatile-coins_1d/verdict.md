---
plan: 031-01.g1.d2_wide-low-close-in-volatile-coins_1d
idea: 031-01.g1.d2_wide-low-close-in-volatile-coins
fit: adapted
status: inconclusive
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move on mean_reversion days with forecast > 0: 0.0186546; t of the mean, cases clustered by day: 3.68712 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: forecast-weighted mean minus unweighted mean of unusual move: -9.61791e-06, passed: False
- Counts: cases: 961, distinct case days: 410
- Decided by: Mean unusual move above 0 with t >= 2, but the supporting check failed.
- Reading: Situation recomputed per window from prices (range = high-low, 20-bar mean range including the day over the day's range <= 0.6667, close location (close-low)/(high-low) <= 0.25, 20-bar log-return std over its 60-bar mean >= 1), active bars lacking that history left out of the agreement; t clusters cases by UTC day (deviations summed per day, small-sample factor G/(G-1)); the plan's 30 distinct case days is treated as a minimum count, giving 'not observable' if unmet.
- Size: unusual move +1.80 % (t 3.65, the cases of one day together: 396 days) per case over 1 bars, 0.335 of the coin's usual move (5.39 %); normal drift in its direction +0.14 %, total +1.94 %; 926 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.g1.d2_wide-low-close-in-volatile-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-01.g1.d2_wide-low-close-in-volatile-coins_1d`
Measure: `measure.py`

---
plan: 060-01.g1.d2.d2_wider-squeeze-day-fades-harder_1d
idea: 060-01.g1.d2.d2_wider-squeeze-day-fades-harder
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move of short cases (return minus coin drift, short-signed): 0.00406483; t of the mean, cases of one day together: 1.83107 (threshold: confirm: mean > 0 with t >= 2 and check difference > 0; reject: mean < 0 with t <= -2)
- Supporting check: upper minus lower half (|forecast| median split) mean unusual move: 0.00622419, passed: True
- Counts: cases: 1380, distinct days: 669
- Decided by: The t lies between -2 and 2.
- Reading: Profile taken from the recorded regime (mean_reversion only when neither chop veto fired, as the detector's 60-day trend and 365-day volatility percentile cannot be rebuilt from the recorded windows) and close location recomputed from prices; day-clustered t uses per-day summed deviations with a G/(G-1) correction; the upper half is |forecast| strictly above the median, the lower half the rest; a minimum count not reached gives 'not observable'.
- Size: unusual move +0.55 % (t 2.13, the cases of one day together: 501 days) per case over 1 bars, 0.113 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.42 %; 954 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d2_wider-squeeze-day-fades-harder_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d2.d2_wider-squeeze-day-fades-harder_1d`
Measure: `measure.py`

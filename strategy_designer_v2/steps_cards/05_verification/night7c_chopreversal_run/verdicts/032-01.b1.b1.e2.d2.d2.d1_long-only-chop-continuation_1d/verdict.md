---
plan: 032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation_1d
idea: 032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-day move on positive-forecast grid bars: 0.0118804; day-clustered t of the mean: 1.34849 (threshold: confirm: mean > 0 with t >= 2 (and tercile difference > 0); reject: t <= -2)
- Supporting check: top minus bottom forecast tercile mean unusual move: 0.0299484, passed: True
- Counts: grid cases with a positive forecast: 532, distinct days: 233
- Decided by: The main t lies between -2 and 2 (inconclusive rule).
- Reading: Situation recomputed per window from closes (ER30 = |close[t]-close[t-30]| / sum of 30 absolute daily changes, 30- and 7-bar simple returns), with the recorded regime=='chop' used only on active bars lacking 30 bars of in-window history; the coin's mean 7-day return is the mean over its non-overlapping grid returns of all windows; terciles split the forecast-sorted cases into three near-equal groups (np.array_split); the day-clustered t uses per-day summed deviations with a D/(D-1) correction; below the minimum counts the status is 'not observable'.
- Size: unusual move +0.99 % (t 1.82, the cases of one day together: 553 days) per case over 7 bars, 0.067 of the coin's usual move (12.44 %); normal drift in its direction +0.89 %, total +1.88 %; 840 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation_1d`
Measure: `measure.py`

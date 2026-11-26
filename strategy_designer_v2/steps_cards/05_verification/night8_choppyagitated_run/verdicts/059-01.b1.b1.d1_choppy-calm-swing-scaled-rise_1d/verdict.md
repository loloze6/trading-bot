---
plan: 059-01.b1.b1.d1_choppy-calm-swing-scaled-rise_1d
idea: 059-01.b1.b1.d1_choppy-calm-swing-scaled-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 14-bar unusual move of the long cases (return minus the coin's normal 14-bar drift): 0.0104527; t of the mean, cases of one day taken together: 0.819701 (threshold: confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of the 14-bar unusual move on the forecast at the signal bar: -0.000633512, passed: False
- Counts: cases: 398, cases on distinct days: 259
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: The choppy calm profile is read from the recorded regime ('trending' only when the detector's trend and swing vetoes did not fire, since its components are not recorded and its 365-bar lookback is not in the record) and the rise from scaled_rise's last_history_value >= 1 (recomputed from prices where missing); a case is the first long bet of each 14-bar grid cell counted from each window's first row, with a 14-bar return inside the window; the day-clustered standard error is sqrt(sum of squared per-day sums of deviations)/n without small-sample correction.
- Size: unusual move +1.05 % (t 0.82, the cases of one day together: 259 days) per case over 14 bars, 0.037 of the coin's usual move (18.92 %); normal drift in its direction +2.21 %, total +3.26 %; 398 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1_choppy-calm-swing-scaled-rise_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1_choppy-calm-swing-scaled-rise_1d`
Measure: `measure.py`

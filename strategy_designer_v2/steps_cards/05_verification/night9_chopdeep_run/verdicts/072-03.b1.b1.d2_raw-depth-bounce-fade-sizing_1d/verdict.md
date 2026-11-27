---
plan: 072-03.b1.b1.d2_raw-depth-bounce-fade-sizing_1d
idea: 072-03.b1.b1.d2_raw-depth-bounce-fade-sizing
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-day move in the short direction: 0.00928238; t clustered by day: 1.37405 (threshold: confirm: mean > 0 with t ≥ 2; reject: t ≤ −2)
- Supporting check: deeper half minus shallower half (median |forecast| at entry): 0.0167608, passed: True
- Counts: cases: 1293, distinct days of cases: 696
- Decided by: The t lies between −2 and 2.
- Reading: Choppy is read as the 60-day close-to-close move within ±10 % (the veto's thresholds read as percent), an up day as a positive one-day close return, below the high as a raw depth < 0, on bars with 60 bars of in-window history (the recorded regime only if none have it); a case is a short bet (|forecast| rising ≥ 2 from its lowest short level since the last bet, from 0 after flat), the first per 10-bar cell counted from each window's first row, needing 10 bars after it in the window; the deeper half is |forecast| above the median and the shallower half at or below it; the clustered t sums the deviations from the mean per UTC day.
- Size: unusual move +0.93 % (t 1.37, the cases of one day together: 696 days) per case over 10 bars, 0.061 of the coin's usual move (16.82 %); normal drift in its direction -1.51 %, total -0.58 %; 1293 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-03.b1.b1.d2_raw-depth-bounce-fade-sizing_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-03.b1.b1.d2_raw-depth-bounce-fade-sizing_1d`
Measure: `measure.py`

---
plan: 032-02.b1_flat-range-upside-break-continues_1d
idea: 032-02.b1_flat-range-upside-break-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move of the bets (drift removed): 0.018471; t of the mean, cases of one day summed: 2.1715 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: slope of unusual 5-day move on entry forecast: -0.00382843, passed: False
- Counts: cases: 232, distinct days: 190
- Decided by: A t >= 2 with a slope of 0 or below is inconclusive.
- Reading: A case is the first bet (forecast rise of at least 2 from its lowest long level since the last bet, reset to 0 when flat) in each 5-bar cell from each window's first row, cases whose 5 bars run past the window's end are dropped, the drift is the coin's mean 5-day return on the same grid pooled over its windows, and the t uses day-summed deviations with a D/(D-1) correction.
- Size: unusual move +1.85 % (t 2.18, the cases of one day together: 190 days) per case over 5 bars, 0.149 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +2.44 %; 232 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1_flat-range-upside-break-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1_flat-range-upside-break-continues_1d`
Measure: `measure.py`

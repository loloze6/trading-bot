---
plan: 032-01.b1.b1_flat-range-breaks-more-coins_1d
idea: 032-01.b1.b1_flat-range-breaks-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 20-bar move after long bets, in the long direction: 0.0577985; t of the mean, cases of one day taken together: 2.52904 (threshold: confirm: mean > 0 with t >= 2 and the supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: above-median minus below-median forecast mean unusual move > 0: -0.0338391, passed: False
- Counts: cases: 294, distinct days: 213
- Decided by: t >= 2 but the supporting check fails
- Reading: the situation is recomputed from each window's own prices (60-bar efficiency ratio of closes <= 0.3 and close above the highest high of the 60 prior bars), active bars without 60 prior bars in their window are left out; a case is the first long bet (a forecast rise of at least 2 points from its low since the last bet, from 0 after a flat) in each 20-bar grid cell counted from each window's first row, with its 20-bar return inside the window; the day-clustered t uses the G/(G-1) correction; cases exactly at the median forecast are left out of the supporting check.
- Size: unusual move +5.78 % (t 2.53, the cases of one day together: 213 days) per case over 20 bars, 0.201 of the coin's usual move (23.78 %); normal drift in its direction +2.93 %, total +8.71 %; 294 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-01.b1.b1_flat-range-breaks-more-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-01.b1.b1_flat-range-breaks-more-coins_1d`
Measure: `measure.py`

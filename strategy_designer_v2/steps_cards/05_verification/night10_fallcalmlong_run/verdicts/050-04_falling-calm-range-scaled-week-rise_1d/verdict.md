---
plan: 050-04_falling-calm-range-scaled-week-rise_1d
idea: 050-04_falling-calm-range-scaled-week-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of the cases: 0.00630669; t of the mean, cases of one day pooled: 1.83431 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: larger-forecast half minus smaller-forecast half mean unusual move: -0.0050965, passed: False
- Counts: distinct days with cases: 342, cases: 496
- Decided by: The main t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first bar in each non-overlapping 3-bar grid cell (from each window's first row) where the forecast rises by at least 2 points above its lowest positive level since the last bet (from 0 after a flat), its return taken from that bar's close over 3 bars inside the window; the t is the mean over its day-clustered standard error (deviations summed per day); the halves are the top and bottom floor(n/2) cases by forecast at the signal, the middle case dropped when n is odd.
- Size: unusual move +0.63 % (t 1.84, the cases of one day together: 342 days) per case over 3 bars, 0.077 of the coin's usual move (8.43 %); normal drift in its direction +0.34 %, total +0.97 %; 496 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.834 (not below 1), 342 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-04_falling-calm-range-scaled-week-rise_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-04_falling-calm-range-scaled-week-rise_1d`
Measure: `measure.py`

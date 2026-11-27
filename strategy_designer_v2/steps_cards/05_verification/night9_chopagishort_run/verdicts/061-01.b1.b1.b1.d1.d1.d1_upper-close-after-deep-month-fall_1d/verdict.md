---
plan: 061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall_1d
idea: 061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-day move per case: 0.0367019; day-clustered t of the mean: 2.87123 (threshold: mean > 0 with day-clustered t >= 2 (and supporting difference > 0) to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: deeper-fall half minus shallower half mean unusual move (split at median |forecast|): 0.00708928, passed: True
- Counts: cases: 145, distinct days: 116
- Decided by: The mean unusual short-side move is above 0 with t >= 2 and the deeper-minus-shallower difference is above 0.
- Reading: Situation check: close location, 5-, 20- and 60-day returns are recomputed from prices inside each window (20-day from the recorded fall20 raw value when present; a condition whose lookback exceeds the window's start is left to the detector), and the 365-day volatility percentile, not computable within a window, is taken from the detector's regime 'mean_reversion'; a case is the first short bet (forecast magnitude rising >= 2 points from its lowest short level since the last bet) in each 5-bar grid cell counted from each window's first row; drift is the coin's mean non-overlapping 5-bar return over all its windows; the clustered t sums deviations per UTC day with a G/(G-1) correction; the deeper half is |forecast| strictly above the cases' median, the shallower half at or below it.
- Size: unusual move +3.67 % (t 2.88, the cases of one day together: 116 days) per case over 5 bars, 0.341 of the coin's usual move (11.68 %); normal drift in its direction -0.67 %, total +3.00 %; 145 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (91 cases, 75 days)
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d1_upper-close-after-deep-month-fall_1d`
Measure: `measure.py`

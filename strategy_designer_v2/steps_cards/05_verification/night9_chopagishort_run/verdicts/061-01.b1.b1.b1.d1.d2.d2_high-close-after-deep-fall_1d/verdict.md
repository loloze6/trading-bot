---
plan: 061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall_1d
idea: 061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-bar move per case: 0.0104129; t of the mean, cases of one day pooled: 2.29702 (threshold: mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: mean unusual move, larger half of |forecast| minus smaller half: 0.00643247, passed: True
- Counts: distinct days with cases: 640, cases: 1853
- Decided by: The mean short-side unusual move is above 0 with t >= 2 and the supporting check passes.
- Reading: A case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, from 0 after flat) in each non-overlapping 5-bar grid cell from each window's first row, needing close[t+5] in the same window; the coin's drift is the mean of its non-overlapping 5-bar returns over all windows; the day-pooled t sums deviations per entry day with a D/(D-1) correction; the halves are the n//2 largest and n//2 smallest |forecast| (middle case dropped if odd); the plan's 100-day minimum, unmet, gives 'not observable'.
- Size: unusual move +1.04 % (t 2.30, the cases of one day together: 640 days) per case over 5 bars, 0.085 of the coin's usual move (12.35 %); normal drift in its direction -0.83 %, total +0.21 %; 1853 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003213 on the check folds against +0.01041 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall_1d`
Measure: `measure.py`

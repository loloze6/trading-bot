---
plan: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall_1d
idea: 061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move in the short direction vs coin drift: 0.0223753; day-clustered t of the mean: 2.70431 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: larger-|forecast| half minus smaller half, mean unusual short move: 0.0237484, passed: True
- Counts: cases: 279, distinct days: 210
- Decided by: The mean unusual short move is positive with t >= 2 and the larger-size half beats the smaller-size half.
- Reading: Profile taken from the recorded regime (not 'chop', the vetoes' result outside the choppy agitated profile) since its 365-bar volatility percentile cannot be rebuilt from the record, close location and 5-day return from prices (5-day return from fall5's raw value where recorded); a case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, reset at flat) in each 5-bar grid cell of a window, with a full 5-bar forward return in that window; drift is the mean of the coin's grid 5-bar returns over all its windows; the day-clustered t uses per-day summed deviations with a D/(D-1) correction; the larger-size half is cases with |forecast| above the median, the smaller-size half those at or below it; the plan's 'fewer than 30 cases or days' is reported as not observable.
- Size: unusual move +2.24 % (t 2.71, the cases of one day together: 210 days) per case over 5 bars, 0.207 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.59 %; 279 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01044 on the check folds against +0.02238 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1_upper-close-after-deep-fall_1d`
Measure: `measure.py`

---
plan: 031-01.b1_up-streak-reversal-more-coins_1d
idea: 031-01.b1_up-streak-reversal-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move after short cases, in the short direction: 0.00269177; t of the mean, cases of one day pooled: 0.865926 (threshold: confirm if day-pooled t >= 2 with supporting check > 0; reject if t <= -2)
- Supporting check: mean unusual move, upper half minus lower half of |forecast| at case: 0.000543282, passed: True
- Counts: distinct case days: 1362, cases: 5838
- Decided by: Main-measure t lies between -2 and 2.
- Reading: A case is the first short bet (forecast rising toward short by >= 2 points from its lowest short level since the last bet, from 0 after flat) in each 5-bar grid cell of its window; the day-pooled t uses per-day summed deviations with a G/(G-1) factor; the median split puts |forecast| above the median in the upper half and at or below it in the lower half; fewer than 100 case days gives 'not observable'.
- Size: unusual move +0.27 % (t 0.87, the cases of one day together: 1362 days) per case over 5 bars, 0.028 of the coin's usual move (11.58 %); normal drift in its direction -0.74 %, total -0.47 %; 5838 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-01.b1_up-streak-reversal-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.b1_up-streak-reversal-more-coins_1d`
Measure: `measure.py`

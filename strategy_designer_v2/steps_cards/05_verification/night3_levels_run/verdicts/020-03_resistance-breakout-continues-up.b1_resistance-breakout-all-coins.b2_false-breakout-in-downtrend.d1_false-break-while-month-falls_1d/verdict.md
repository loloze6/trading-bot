---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean excess fall of the short over 10 days, cut at the first day the 30-day return is >= 0, minus the coin's daily drift: 0.0126182; t of the mean: 0.968857 (threshold: confirm: mean > 0 with t >= 2 and deeper-minus-shallower > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: deeper-half minus shallower-half mean excess fall (split at median 30-day return): 0.0205482, passed: True
- Counts: cases: 106, deeper_half: 53, shallower_half: 53
- Decided by: The t of the mean excess fall lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is taken as regime == 'mean_reversion' (the detector's recorded decision on the break, the >=3 touch count and the falling month, whose components are not recorded) plus a negative 30-day return (recorded 'decline' raw value, else recomputed from closes) with a short forecast; a case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet) in each 10-bar grid cell of a window with all 10 following bars in the window; the stop day's return is included, the 30-day return on each day is recomputed from the window's closes (falling back to the recorded value when 30 past bars are not in the window, and not stopping when neither exists); drift is the coin's mean daily return over all its windows times the days counted; the depth split uses the recorded 30-day return on the signal bar, deeper = strictly below the median.
- Size: unusual move +0.30 % per case over 10 bars, -0.038 of the coin's usual move (16.61 %); normal drift in its direction -1.31 %, total -1.01 %; 106 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d`
Measure: `measure.py`

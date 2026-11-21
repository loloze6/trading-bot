---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted 10-bar fall after short cases: 0.0178956; t of the mean: 4.05467 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and deeper-half minus shallower-half > 0; reject: mean is a rise with t <= -2 over >= 30 cases)
- Supporting check: deeper-decline half minus shallower half, mean drift-adjusted fall: 0.0300497, passed: True
- Counts: cases: 1230, deeper-half cases: 425, shallower-half cases: 425
- Decided by: The mean drift-adjusted fall is above 0 with t >= 2 over at least 30 cases, and the deeper-decline half falls more.
- Reading: The plan's situation is computed as a fresh resistance break (raw break component > 0) on a bar whose 30-bar close-to-close return is below 0 (from the window's closes, or the recorded regime where 30 past closes are not in the window), on the short side; a case is a short bet of the forecast (a rise of at least 2 points on the short side), the first one per 10-bar grid cell from each window's first row, with the drift the mean of the coin's grid 10-bar returns over all windows; the deeper-decline half is the cases with 30-bar return below the median, the rest the shallower half; the plan's 'fewer than 30 cases' is applied as the minimum count (not observable).
- Size: unusual move +1.79 % per case over 10 bars, 0.098 of the coin's usual move (16.53 %); normal drift in its direction -1.38 %, total +0.41 %; 1230 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d`
Measure: `measure.py`

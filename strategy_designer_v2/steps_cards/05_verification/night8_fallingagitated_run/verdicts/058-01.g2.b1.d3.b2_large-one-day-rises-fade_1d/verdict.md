---
plan: 058-01.g2.b1.d3.b2_large-one-day-rises-fade_1d
idea: 058-01.g2.b1.d3.b2_large-one-day-rises-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move after short bets, in the short direction: 0.0139815; t of the mean, cases grouped by day: 1.84135 (threshold: confirm: mean > 0 with t >= 2 and size check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above minus below the cases' median |forecast|: 0.00701371, passed: True
- Counts: cases: 449, distinct days: 202
- Decided by: The t lies between -2 and 2 (inconclusive rule).
- Reading: The situation is checked as a raw scaled rise >= 1.0 (recorded last_history_value, recomputed from closes with a 30-return ddof-1 std including the day where missing) with a negative forecast, the falling-agitated profile not being recomputable from the record (365-bar percentile, warm-up not recorded); a case is the first short bet (forecast magnitude rising by >= 2 from its lowest short level since the last bet, from 0 after flat) in each 5-bar grid cell of a window, drift is the mean of the coin's grid 5-bar returns over all its windows, the day t sums deviations per UTC day, and the size check splits strictly above/below the cases' median |forecast|.
- Size: unusual move +1.40 % (t 1.84, the cases of one day together: 202 days) per case over 5 bars, 0.116 of the coin's usual move (11.68 %); normal drift in its direction -0.75 %, total +0.65 %; 449 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d3.b2_large-one-day-rises-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d3.b2_large-one-day-rises-fade_1d`
Measure: `measure.py`

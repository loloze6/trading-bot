---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of pooled 10-day excess return on forecast: 2.17634; OLS slope t: 2.17634 (threshold: confirm if slope t >= 2 and the check passes; reject if slope t <= -2)
- Supporting check: mean excess 10-day return of cases above the in-regime median forecast: 0.00964778, passed: True
- Counts: in-regime cases: 820, cases above the median: 410, cases at or below the median: 410
- Decided by: Confirm: the slope t is 2 or more and the above-median cases' mean excess return is above 0.
- Reading: The 20-day return is recomputed from closes inside each window, with the recorded regime used on the first 20 bars of a window where it cannot be computed; the in-regime median is the median forecast over the in-regime cases, 'above' is strictly above it and the other side is at or below it; a case needs its 10-day return inside its window; the plan's minimum counts, when not reached, give 'not observable' as the workflow requires.
- Size: unusual move +0.75 % per case over 10 bars, 0.047 of the coin's usual move (14.49 %); normal drift in its direction +1.18 %, total +1.93 %; 1178 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise_1d`
Measure: `measure.py`

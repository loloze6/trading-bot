---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 5-bar excess return on forecast (pooled, non-overlapping grid): 2.56085; OLS slope t: 2.56085 (threshold: confirm if t >= 2 with timing > 0; reject if t <= -2; else inconclusive; at least 500 non-overlapping cases with non-zero forecast)
- Supporting check: book timing (mean daily gain before costs minus market-rise part): 0.00011136, passed: True
- Counts: non-overlapping cases with a non-zero forecast: 3419, non-overlapping cases: 3419
- Decided by: The slope's t is 2 or more and timing is above 0.
- Reading: The regression uses every grid bar (forecast zero included) with a complete 5-bar return inside its window, the drift is each coin's mean grid 5-bar return over all windows, the book before costs is position held x next-bar coin return averaged over coins per day, and the plan's 'fewer than 500 cases' minimum is applied as 'not observable'.
- Size: unusual move +0.59 % per case over 5 bars, 0.051 of the coin's usual move (10.60 %); normal drift in its direction -0.04 %, total +0.55 %; 2752 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d`
Measure: `measure.py`

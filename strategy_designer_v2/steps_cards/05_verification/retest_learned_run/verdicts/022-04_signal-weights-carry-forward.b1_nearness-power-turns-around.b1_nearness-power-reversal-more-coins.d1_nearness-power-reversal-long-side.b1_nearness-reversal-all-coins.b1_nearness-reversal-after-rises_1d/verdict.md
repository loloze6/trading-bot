---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar return minus coin's normal 5-bar drift on forecast: 0.000626973; OLS slope t: 1.99122 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 100 grid cases with forecast > 0)
- Supporting check: book's timing gain before costs (mean daily gain minus coin-rise part): 0.00029948, passed: True
- Counts: grid cases with a forecast above 0: 1127, grid cases: 4875
- Decided by: The slope's t lies between -2 and 2 (no confirm or reject rule met).
- Reading: All grid cases (forecast 0 included) enter the pooled regression, the drift is each coin's mean non-overlapping 5-bar return over all its windows, and the timing gain uses the position before costs (allocation x next-bar return) minus allocation x the coin's mean daily return, averaged over coins per day then over days.
- Size: unusual move +0.84 % per case over 5 bars, 0.071 of the coin's usual move (11.16 %); normal drift in its direction +0.68 %, total +1.52 %; 840 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d`
Measure: `measure.py`

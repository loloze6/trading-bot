---
plan: 072-03.b1.b1.d1_deep-bounce-in-decline-fades_1d
idea: 072-03.b1.b1.d1_deep-bounce-in-decline-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move in the short direction: 0.0148557; t of the mean, cases clustered by day: 1.78654 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: deeper half minus shallower half mean unusual move: -0.00478189, passed: False
- Counts: cases: 742, distinct days carrying cases: 435
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Day return and 20-bar return are recomputed from closes inside each window (the regime column stands in where the lookback precedes the window's first bar) and the choppy profile is read as regime != 'chop'; a short bet is a fall of the forecast of at least 2 points from its shallowest short level since the last bet (from 0 after flat), the first bet of each 10-bar grid cell counts as the case, the drift is the coin's mean 10-bar return on the grid of all its windows, the t clusters deviations by UTC day, and the deeper half is |forecast| strictly above the cases' median against the rest.
- Size: unusual move +1.49 % (t 1.79, the cases of one day together: 435 days) per case over 10 bars, 0.079 of the coin's usual move (16.82 %); normal drift in its direction -1.47 %, total +0.01 %; 742 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-03.b1.b1.d1_deep-bounce-in-decline-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-03.b1.b1.d1_deep-bounce-in-decline-fades_1d`
Measure: `measure.py`

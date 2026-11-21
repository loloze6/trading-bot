---
plan: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next 10-bar return minus coin drift on forecast (non-overlapping grid, pooled): 0.00193829; OLS slope t: 2.69253 (threshold: confirm: t >= 2 with timing gain > 0; reject: t <= -2; at least 300 non-overlapping cases)
- Supporting check: book's timing gain before costs (mean daily return minus market part): 0.000322453, passed: True
- Counts: non-overlapping cases: 1691, active bars: 17524
- Decided by: The slope's t is 2 or more and the timing gain is above 0.
- Reading: Every bar is a bar of the graded situation, its expected side being the sign of the sum rebuilt from the raw components with the engine's standardise (recorded post-pipeline values where fewer than a full window of past raw values is recorded); the regression is OLS with intercept over all grid bars with a forecast and a full 10-bar return; the drift is the coin's mean grid 10-bar return; the timing gain is the mean over days of the coins' mean of position x (daily return minus the coin's mean daily return), before costs; fewer than 300 cases gives 'not observable'.
- Size: unusual move +1.41 % per case over 10 bars, 0.088 of the coin's usual move (14.49 %); normal drift in its direction +0.11 %, total +1.52 %; 1206 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d`
Measure: `measure.py`

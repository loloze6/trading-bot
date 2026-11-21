---
plan: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed 5-bar forward return on forecast: 0.000830203; OLS slope t: 2.37 (threshold: t >= 2 confirms (with top-minus-bottom fifth > 0); t <= -2 rejects)
- Supporting check: top-minus-bottom fifth drift-removed 5-bar return: 0.0115216, passed: True
- Counts: non-overlapping grid cases with a non-zero forecast: 3419, top fifth cases: 683, bottom fifth cases: 683
- Decided by: The slope's t is 2 or more and the top-minus-bottom-fifth difference is positive.
- Reading: The slope, its t and the fifths use the non-overlapping 5-bar grid bars (positions 0,5,10,... of each window) with a non-zero forecast, pooled; the drift is the coin's mean 5-bar grid return over all its windows; the fifths are the n//5 lowest and highest forecasts after sorting; the slope's t is the OLS t with an intercept.
- Size: unusual move +0.83 % per case over 5 bars, 0.071 of the coin's usual move (10.60 %); normal drift in its direction +0.06 %, total +0.89 %; 1706 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d`
Measure: `measure.py`

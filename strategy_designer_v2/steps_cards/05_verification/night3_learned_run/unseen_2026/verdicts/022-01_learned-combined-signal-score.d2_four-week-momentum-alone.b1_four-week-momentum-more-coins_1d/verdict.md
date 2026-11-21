---
plan: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-day excess return on the mom28 post-pipeline forecast, pooled: 0.000460725; OLS slope t: 1.79012 (threshold: confirm if t >= 2 (with top-minus-bottom fifth > 0); reject if t <= -2; otherwise inconclusive; at least 300 grid cases)
- Supporting check: mean excess 5-day return, top fifth minus bottom fifth of forecasts: 0.0221734, passed: True
- Counts: grid cases with a recorded forecast: 1178, top fifth cases: 235, bottom fifth cases: 235
- Decided by: The slope's t is between -2 and 2.
- Reading: Grid cases are window rows 0, 5, 10, ... with a full in-window 5-bar forward return; the coin's mean is taken over all its grid cases in all windows; the top and bottom fifths are the floor(n/5) highest and lowest forecasts after a stable sort; the plan's 'fewer than 300 is inconclusive' is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.64 % per case over 5 bars, 0.064 of the coin's usual move (9.44 %); normal drift in its direction +0.05 %, total +0.68 %; 827 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d`
Measure: `measure.py`

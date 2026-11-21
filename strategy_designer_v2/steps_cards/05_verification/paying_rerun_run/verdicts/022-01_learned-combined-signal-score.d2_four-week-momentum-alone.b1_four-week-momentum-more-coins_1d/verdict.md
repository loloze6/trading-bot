---
plan: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-day excess return on the mom28 post-pipeline forecast, pooled: 0.000493642; OLS slope t: 3.64065 (threshold: confirm if t >= 2 (with top-minus-bottom fifth > 0); reject if t <= -2; otherwise inconclusive; at least 300 grid cases)
- Supporting check: mean excess 5-day return, top fifth minus bottom fifth of forecasts: 0.0130051, passed: True
- Counts: grid cases with a recorded forecast: 7270, top fifth cases: 1454, bottom fifth cases: 1454
- Decided by: The slope's t is 2 or more and the top-minus-bottom-fifth excess return difference is above 0.
- Reading: Grid cases are window rows 0, 5, 10, ... with a full in-window 5-bar forward return; the coin's mean is taken over all its grid cases in all windows; the top and bottom fifths are the floor(n/5) highest and lowest forecasts after a stable sort; the plan's 'fewer than 300 is inconclusive' is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.66 % per case over 5 bars, 0.046 of the coin's usual move (12.35 %); normal drift in its direction -0.04 %, total +0.62 %; 5202 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d`
Measure: `measure.py`

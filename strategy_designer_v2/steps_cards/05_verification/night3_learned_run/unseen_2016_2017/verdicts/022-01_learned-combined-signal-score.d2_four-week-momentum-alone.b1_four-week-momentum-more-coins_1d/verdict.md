---
plan: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-day excess return on the mom28 post-pipeline forecast, pooled: 0.00227723; OLS slope t: 3.08666 (threshold: confirm if t >= 2 (with top-minus-bottom fifth > 0); reject if t <= -2; otherwise inconclusive; at least 300 grid cases)
- Supporting check: mean excess 5-day return, top fifth minus bottom fifth of forecasts: 0.066254, passed: True
- Counts: grid cases with a recorded forecast: 572, top fifth cases: 114, bottom fifth cases: 114
- Decided by: The slope's t is 2 or more and the top-minus-bottom-fifth excess return difference is above 0.
- Reading: Grid cases are window rows 0, 5, 10, ... with a full in-window 5-bar forward return; the coin's mean is taken over all its grid cases in all windows; the top and bottom fifths are the floor(n/5) highest and lowest forecasts after a stable sort; the plan's 'fewer than 300 is inconclusive' is reported as 'not observable' as the workflow requires.
- Size: unusual move +2.81 % per case over 5 bars, 0.144 of the coin's usual move (18.32 %); normal drift in its direction +1.27 %, total +4.08 %; 394 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d`
Measure: `measure.py`

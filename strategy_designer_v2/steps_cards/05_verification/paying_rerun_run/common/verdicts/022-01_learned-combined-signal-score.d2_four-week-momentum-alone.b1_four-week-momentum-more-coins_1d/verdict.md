---
plan: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-day excess return on the mom28 post-pipeline forecast, pooled: 0.000569746; OLS slope t: 5.01736 (threshold: confirm if t >= 2 (with top-minus-bottom fifth > 0); reject if t <= -2; otherwise inconclusive; at least 300 grid cases)
- Supporting check: mean excess 5-day return, top fifth minus bottom fifth of forecasts: 0.0177491, passed: True
- Counts: grid cases with a recorded forecast: 10967, top fifth cases: 2193, bottom fifth cases: 2193
- Decided by: The slope's t is 2 or more and the top-minus-bottom-fifth excess return difference is above 0.
- Reading: Grid cases are window rows 0, 5, 10, ... with a full in-window 5-bar forward return; the coin's mean is taken over all its grid cases in all windows; the top and bottom fifths are the floor(n/5) highest and lowest forecasts after a stable sort; the plan's 'fewer than 300 is inconclusive' is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.71 % (t 2.53, the cases of one day together: 2252 days) per case over 5 bars, 0.047 of the coin's usual move (12.26 %); normal drift in its direction -0.01 %, total +0.70 %; 7890 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d`
Measure: `measure.py`

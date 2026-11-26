---
plan: 063-01_calm-big-up-day-continues_1d
idea: 063-01_calm-big-up-day-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-bar return on scaled_rise post_pipeline_value, in-profile grid bars: 0.00175408; slope t: 5.21924 (threshold: confirm if t >= 2 (with supporting mean > 0); reject if t <= -2)
- Supporting check: mean excess 5-bar return on grid cases with forecast >= 10: 0.0183751, passed: True
- Counts: grid cases: 1829, grid cases with forecast above 0: 897, grid cases with forecast at or above 10: 407
- Decided by: The slope's t is 2 or more and the mean excess return at forecast >= 10 is above 0.
- Reading: In-profile bars are those with regime 'unknown' (calm, not vetoed to 'chop'), the coin's drift is its mean 5-bar return on the 0,5,10,... grid of all its windows, the plan's 'else inconclusive' minimum of 100 positive-forecast cases is applied as 'not observable' per the workflow, and a missing supporting mean counts as not above 0.
- Size: unusual move +0.01 % (t 0.02, the cases of one day together: 822 days) per case over 5 bars, -0.003 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +0.64 %; 1765 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001325 on the check folds against +0.001754 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/063-01_calm-big-up-day-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/063-01_calm-big-up-day-continues_1d`
Measure: `measure.py`

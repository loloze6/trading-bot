---
plan: 058-01.b1_calm-downtrend-all-coins_1d
idea: 058-01.b1_calm-downtrend-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on short size (-forecast), day-clustered t: -0.000435884; slope t, cases of one day summed (day-clustered): -0.60512 (threshold: confirm: slope < 0 with t <= -2 and mean excess < 0; reject: slope > 0 with t >= +2)
- Supporting check: mean excess return of the short cases below 0: -0.00187315, passed: True
- Counts: grid cases with forecast < 0: 981, distinct days: 271
- Decided by: Inconclusive rule: the slope t lies between -2 and +2.
- Reading: Grid bars at positions 0,5,10,... per window with a full 5-bar return; the coin's drift is the mean of all its grid 5-bar returns over all windows; the slope t uses day-clustered OLS standard errors (score sums per UTC day, G/(G-1) correction); the profile is the recorded regime 'unknown'; and short counts follow the instructions' 'not observable' for the plan's minimums.
- Size: unusual move +0.79 % (t 1.63, the cases of one day together: 519 days) per case over 5 bars, 0.067 of the coin's usual move (11.68 %); normal drift in its direction -0.66 %, total +0.13 %; 993 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01.b1_calm-downtrend-all-coins_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.b1_calm-downtrend-all-coins_1d`
Measure: `measure.py`

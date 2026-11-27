---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar excess return on signal-bar forecast: 0.00401754; OLS slope t: 2.13062 (threshold: slope t >= 2 with mean excess > 0 confirms; slope t <= -2 rejects; at least 100 cases)
- Supporting check: mean excess 10-bar return over all cases above 0: 0.043737, passed: True
- Counts: cases: 1619
- Decided by: The slope's t is 2 or more and the mean excess return of the cases is above 0.
- Reading: A case is the first bar in each 10-bar grid cell (counted from each window's first row) where the long forecast rises at least 2 points above its lowest level since the last such rise (reset to 0 when flat, starting from 0 at each window's start), cases whose 10-bar return would leave the window are dropped, the drift is the coin's mean return on the non-overlapping 10-bar grid of all its windows, and the plan's fewer-than-100-cases rule is reported as not observable.
- Size: unusual move +4.37 % (t 4.59, the cases of one day together: 818 days) per case over 10 bars, 0.222 of the coin's usual move (16.74 %); normal drift in its direction +1.52 %, total +5.89 %; 1619 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d`
Measure: `measure.py`

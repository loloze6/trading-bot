---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar excess return on signal-bar forecast: 0.00665272; OLS slope t: 3.23516 (threshold: slope t >= 2 with mean excess > 0 confirms; slope t <= -2 rejects; at least 100 cases)
- Supporting check: mean excess 10-bar return over all cases above 0: 0.033861, passed: True
- Counts: cases: 1129
- Decided by: The slope's t is 2 or more and the mean excess return of the cases is above 0.
- Reading: A case is the first bar in each 10-bar grid cell (counted from each window's first row) where the long forecast rises at least 2 points above its lowest level since the last such rise (reset to 0 when flat, starting from 0 at each window's start), cases whose 10-bar return would leave the window are dropped, the drift is the coin's mean return on the non-overlapping 10-bar grid of all its windows, and the plan's fewer-than-100-cases rule is reported as not observable.
- Size: unusual move +3.39 % per case over 10 bars, 0.175 of the coin's usual move (16.82 %); normal drift in its direction +1.50 %, total +4.89 %; 1129 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d`
Measure: `measure.py`

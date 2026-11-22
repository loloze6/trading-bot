---
plan: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d
idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-day move over short-bet cases: 0.00611928; t of the mean: 2.78795 (threshold: mean > 0 with t >= 2 confirms (with slope t >= 2); t <= -2 rejects)
- Supporting check: slope t of unusual move on fall90 raw 90-day return: 2.27041, passed: True
- Counts: cases: 2303, cases with fall90 recorded: 2303
- Decided by: Confirm rule met: mean unusual short move positive with t >= 2 and slope t >= 2.
- Reading: A case is the first bar in each non-overlapping 5-bar grid cell of a window where the forecast falls at least 2 points below its least-negative level since the last short bet (from 0 after flat), its move is -(close[t+5]/close[t]-1 - the coin's mean grid 5-bar return over all windows), the slope's t is the OLS slope over its standard error on fall90's raw last_history_value, and the plan's 30-case minimum is reported as not observable.
- Size: unusual move +0.61 % per case over 5 bars, 0.047 of the coin's usual move (12.24 %); normal drift in its direction -0.74 %, total -0.13 %; 2303 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d`
Measure: `measure.py`

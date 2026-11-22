---
plan: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d
idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move in the short direction after short bets: 0.00615611; t of the mean: 2.81011 (threshold: confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2)
- Supporting check: Pearson correlation of forecast size with the unusual short move: -0.0278581, passed: False
- Counts: cases over all coins and windows: 2312
- Decided by: The mean unusual short move is positive with t >= 2 but the correlation is 0 or below.
- Reading: The 90-day fall is recomputed as close[t]/close[t-90]-1 inside the window where 90 prior bars exist and taken from regime == 'mean_reversion' elsewhere, the rise is the bounce component's raw value > 0; a short bet is a fall of the forecast of at least 2 points from its least-short level on the short side since the last bet (from 0 after flat or long), the case of a grid cell is its first bet with a full 5-bar return inside the window, and the forecast's size is its absolute value.
- Size: unusual move +0.62 % per case over 5 bars, 0.047 of the coin's usual move (12.45 %); normal drift in its direction -0.76 %, total -0.14 %; 2312 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d`
Measure: `measure.py`

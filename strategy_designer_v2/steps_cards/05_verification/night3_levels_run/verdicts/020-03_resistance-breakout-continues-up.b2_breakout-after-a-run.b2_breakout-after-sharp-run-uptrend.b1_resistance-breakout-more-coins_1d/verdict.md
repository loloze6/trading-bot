---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar excess return of long bets over the coin's mean 5-bar return: 0.00426072; t of the mean: 1.42215 (threshold: confirm t >= 2, reject t <= -2, over at least 30 cases)
- Supporting check: forecast-weighted mean excess minus unweighted mean excess (> 0): 0.0027024, passed: True
- Counts: cases: 2511
- Decided by: Mean excess return t between -2 and 2 over at least 30 cases.
- Reading: Situation = break component raw value > 0 and 60-bar close return (recomputed within the window) > 0, side long; active bars whose 60-bar return cannot be computed inside the window are left out of the agreement, a missing break value counts as outside the situation; a case is the first long bet (forecast rise >= 2 points from its lowest positive level since the last bet, from 0 after flat) in each 5-bar grid cell of a window, its excess return is the 5-bar return from that bar minus the coin's mean 5-bar return on the non-overlapping grid of all its windows, and the supporting check weights by the forecast on the signal bar.
- Size: unusual move +0.43 % per case over 5 bars, 0.031 of the coin's usual move (12.24 %); normal drift in its direction +0.74 %, total +1.17 %; 2511 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d`
Measure: `measure.py`

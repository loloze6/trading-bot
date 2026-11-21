---
plan: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return over coin drift of long bets: 0.00236252; t of the mean: 0.967835 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: Spearman(forecast width, excess return) > 0: 0.0779664, passed: True
- Counts: independent cases: 1182
- Decided by: The t of the mean excess return lies between -2 and 2.
- Reading: The situation is recomputed from prices as close below the minimum low of the 12 prior bars and close/close 180 bars earlier minus 1 above 0, inside each window, leaving out active bars without 180 bars of in-window history; a case is the first long bet (forecast rise of at least 2 points from its lowest level since the last bet, from 0 after a flat) in each 18-bar grid cell of each window, with cases pooled over all coins and each coin's drift the mean of its non-overlapping 18-bar grid returns over all its windows; fewer than 30 cases is reported as not observable.
- Size: unusual move +0.24 % per case over 18 bars, 0.023 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.64 %; 1182 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h`
Measure: `measure.py`

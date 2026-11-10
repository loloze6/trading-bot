---
plan: 001-01_rsi-high-extreme-reversal-down_1h
idea: 001-01_rsi-high-extreme-reversal-down
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 12-bar log excess return after top-decile |forecast| bars: -0.00143263; t of the mean on non-overlapping 12-bar blocks: -1.23079 (threshold: confirm: negative with t <= -2 and negative in >= 2 coins; reject: positive with t >= +2; else inconclusive; needs >= 30 episodes per coin and >= 100 pooled)
- Supporting check: excess return falls steadily from zero-forecast group through |forecast| quintiles (Spearman rho), same sign in >= 2 coins: None, passed: None
- Counts: pooled non-overlapping extreme episodes: 390, non-overlapping extreme episodes BTCUSD: 187, non-overlapping extreme episodes ETHUSD: 203, coins with negative excess: 2, coins in record: 2
- Decided by: The pooled t lies between -2 and +2.
- Reading: Top decile is the pooled 90th percentile of |forecast| over all bars of all coins and windows (non-zero only), excess is each bar's forward 12-bar log return minus its coin-window mean over all bars, sampled on the 0,12,24,... grid with the ordinary t of the mean; with only 2 coins in the record, 'at least 2 of 3 coins' is read as both coins, and 'fall steadily' as strictly decreasing pooled means over neutral then quintiles 1-5, with a negative per-coin Spearman slope in at least 2 coins.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-01_rsi-high-extreme-reversal-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-01_rsi-high-extreme-reversal-down_1h`
Measure: `measure.py`

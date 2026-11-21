---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed 72-bar excess return on grid bars with |forecast| >= 10 in mean_reversion: 0.00746366; ordinary t: 1.35258 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: slope of signed excess return on |forecast|, grid bars in regime with forecast != 0: 0.000409366, passed: True
- Counts: independent cases pooled: 195, cases on BTCUSD: 96, cases on ETHUSD: 99, grid bars in regime with forecast != 0 (supporting): 813
- Decided by: t lies between -2 and 2.
- Reading: The coin's mean 72-bar return is the mean over all its non-overlapping grid returns across all windows, grid bars without a bar t+72 in the same window are dropped, and the plan's minimum counts are applied as 'not observable' per the workflow.
- Size: unusual move -0.30 % per case over 72 bars, -0.039 of the coin's usual move (7.02 %); normal drift in its direction -0.03 %, total -0.33 %; 883 cases
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h`
Measure: `measure.py`

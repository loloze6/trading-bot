---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of mild minus deep excess 10-bar return: -0.0194432; Welch t: -0.812324 (threshold: confirm if t <= -2 (with mild mean excess < 0); reject if t >= +2)
- Supporting check: mild group mean excess 10-bar return below 0: -0.0274015, passed: True
- Counts: cases in total: 135, mild group cases: 68, deep group cases: 67
- Decided by: The Welch t of mild minus deep lies between -2 and +2.
- Reading: The new-low situation is recomputed inside each window as the close below every one of the prior 30 closes, using the available prior closes for bars with fewer than 30 in-window predecessors and skipping each window's first bar; the coin's mean 10-bar return is taken on the non-overlapping grid (positions 0, 10, 20, ...) of all its windows pooled; the median split uses the pooled cases of both coins; and fewer than 20 cases per group or 40 in total is reported as 'not observable' as the workflow requires.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d`
Measure: `measure.py`

---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 20-bar fwd return with forecast > 0 minus mean over all bars (non-overlapping): 0.0282881; Welch t: 0.790345 (threshold: difference above 0 with t >= 2)
- Supporting check: up-cross positive 20-bar return share minus unconditional positive share: 0.436066, passed: True
- Counts: non-overlapping in-position blocks: 13, up-crosses: 2, non-overlapping all-bars blocks: 34
- Decided by: Fewer than the required 15 non-overlapping in-position blocks or 8 up-crosses (have 13 and 2), so the test neither confirms nor rejects.
- Reading: In-position and all-bars groups share one grid per window at rows 0,20,40,... compared by Welch t; an up-cross is a bar with forecast > 0 whose previous bar in the same window has forecast <= 0, counted only when its 20-bar forward return exists; the unconditional share uses every bar's 20-bar forward return within each window; a reversal means the mean up-cross forward return is below 0.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`

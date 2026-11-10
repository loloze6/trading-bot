---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 20-bar fwd return in-position minus all bars (non-overlapping): 0.0282881; Welch t: 0.790345 (threshold: difference above 0 with t >= 2 to confirm; difference <= 0 rejects)
- Supporting check: up-cross positive 20-bar share minus unconditional share: 0.436066, passed: True
- Counts: non-overlapping in-position blocks: 13, up-crosses: 2
- Decided by: Fewer than the required minimums (13 in-position non-overlapping blocks vs 15, 2 up-crosses vs 8), so the test neither confirms nor rejects.
- Reading: Pooled all windows of every coin present, used the 0,20,40,... grid per window for both groups with Welch t, counted an up-cross as a bar with forecast > 0 after a bar with forecast <= 0 inside the same window that has a full 20-bar forward return, took the unconditional share over every bar with a valid 20-bar forward return, and applied the minimum counts first, then reject, then confirm.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`

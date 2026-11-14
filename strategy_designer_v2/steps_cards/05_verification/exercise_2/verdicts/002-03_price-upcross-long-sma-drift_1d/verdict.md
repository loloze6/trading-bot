---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 20-bar fwd return in position minus all bars (non-overlapping blocks), t=1.102: 0.0282881 (threshold: above 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: share of positive 20-bar returns after up-crosses minus unconditional share: 0.436066, passed: True
- Cases: 13
- Decided by: Fewer than 15 non-overlapping in-position blocks (13) or fewer than 8 up-crosses (2), so the test neither confirms nor rejects.
- Reading: Blocks start at each window's first bar every 20 bars (block in position if forecast > 0 at its start), t is the one-sample t of in-position block returns minus the all-blocks mean, up-crosses are bars with forecast > 0 after a bar with forecast <= 0 in the same window, and the unconditional positive share uses every bar's 20-bar forward return pooled over all windows.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`

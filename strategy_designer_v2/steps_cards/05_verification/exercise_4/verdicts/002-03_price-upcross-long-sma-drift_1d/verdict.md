---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 20-bar fwd return in position minus all bars: 0.0282881; Welch t: 0.790345 (threshold: difference above 0 with t >= 2)
- Supporting check: share of positive 20-bar returns after up-crosses minus unconditional share: 0.436066, passed: True
- Counts: non-overlapping in-position blocks: 13, non-overlapping all-bars blocks: 34, up-crosses: 2, mean 20-bar return after up-crosses: 0.203853, share positive after up-crosses: 1, unconditional share positive: 0.563934
- Decided by: Fewer than 15 non-overlapping in-position blocks or fewer than 8 up-crosses, so the test neither confirms nor rejects.
- Reading: Blocks are the bars at positions 0, 20, 40, ... of each window, with in-position meaning forecast > 0 on the block's first bar, compared by Welch t against all grid bars. An up-cross is a bar with forecast > 0 whose previous bar in the same window has forecast <= 0, counted only when it has a full 20-bar forward return. The unconditional share uses every bar with a valid 20-bar forward return.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`

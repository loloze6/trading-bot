---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 20-bar fwd return on forecast>0 blocks minus mean over all blocks: 0.0282881 (threshold: above 0 with t >= 2 (t = 1.102))
- Supporting check: share of up-crosses with positive 20-bar return vs unconditional share (1.0 vs 0.5639344262295082; mean after cross 0.20385257859389416): 1, passed: True
- Cases: 13
- Decided by: Fewer than the minimum counts (13 in-position blocks vs 15 needed, 2 up-crosses vs 8 needed), so the test neither confirms nor rejects.
- Reading: Non-overlapping blocks start at each window's first bar every 20 bars, a block is in-position when forecast > 0 at its start bar, t is the difference divided by the standard error of the in-position block returns, an up-cross is forecast <= 0 on the prior bar and > 0 on the bar, and the unconditional share uses the 20-bar forward returns of every bar in the windows.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`

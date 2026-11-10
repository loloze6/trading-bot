---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar fwd return in position minus all bars (non-overlapping): 0.0282881; Welch t: 0.790345 (threshold: difference > 0 with Welch t >= 2 across non-overlapping 20-bar blocks)
- Supporting check: share of positive 20-bar returns after up-crosses minus unconditional share: 0.436066, passed: True
- Counts: non-overlapping in-position blocks: 13, up-crosses: 2
- Decided by: Fewer than 15 non-overlapping in-position blocks or fewer than 8 up-crosses, so the test neither confirms nor rejects.
- Reading: Close above SMA200 taken as the raw component value > 0 (column debug_info.components.above_sma200.last_history_value); the all-bars group is every grid bar (positions 0,20,40,... per window) and Welch's t compares it with the in-position grid bars; up-crosses are bars with forecast > 0 whose previous bar in the same window had forecast 0, counted only when their 20-bar forward return exists, and the unconditional share of positive returns uses all bars with a 20-bar forward return.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`

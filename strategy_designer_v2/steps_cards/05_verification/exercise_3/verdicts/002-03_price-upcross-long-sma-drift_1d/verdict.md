---
plan: 002-03_price-upcross-long-sma-drift_1d
idea: 002-03_price-upcross-long-sma-drift
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 20-bar fwd return, forecast>0 minus all bars: 0.0282881; Welch t: 0.790345 (threshold: difference > 0 with t >= 2 across non-overlapping 20-bar blocks)
- Supporting check: share positive 20-bar returns after up-crosses minus unconditional share: 0.529412, passed: True
- Counts: non-overlapping in-position blocks: 13, up-crosses: 2, non-overlapping all-bars blocks: 34
- Decided by: Fewer than 15 non-overlapping in-position blocks or fewer than 8 up-crosses, so the test neither confirms nor rejects.
- Reading: Up-crosses are bars with forecast > 0 whose prior bar in the same window had forecast <= 0, each with its own 20-bar forward return (overlap allowed); the unconditional share of positive returns and the all-bars mean use the same non-overlapping grid (positions 0, 20, 40, ... per window); the t is Welch's between in-position and all-bars blocks; the reversal reject is checked before the confirm rule.
Plan: `steps_cards/03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-upcross-long-sma-drift_1d`
Measure: `measure.py`

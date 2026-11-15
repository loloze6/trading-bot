---
plan: 002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad_1d
idea: 002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next 1-bar return minus coin mean, on forecast > 0 bars: 1.56518e-05; t of the mean: 0.0322316 (threshold: confirm t >= 2 (with up-share above coin's), reject t <= -2)
- Supporting check: up-bar share on forecast > 0 bars minus coin overall up-share: -0.000854711, passed: False
- Counts: bars with forecast > 0: 12451
- Decided by: The t of the mean excess return lies between -2 and 2.
- Reading: Situation is bars where the raw SMA50-SMA200 spread (last_history_value) is > 0, on the long side, and bars with a missing spread are left out of the agreement; the next 1-bar return is taken on every bar inside its window, the coin's mean and up-share use all of its bars over all windows, and the supporting check compares the pooled up-share of forecast > 0 bars with the same bars' coin overall up-shares (mean of up minus the coin's share > 0).
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift.a1_sma-up-stretch-drift-broad_1d`
Measure: `measure.py`

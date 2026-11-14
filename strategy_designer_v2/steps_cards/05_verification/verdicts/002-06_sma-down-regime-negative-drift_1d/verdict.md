---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean of next-bar return minus coin mean, short bars: -0.00100349; t of weighted mean: -0.538966 (threshold: t <= -2 with negative mean confirms; t >= +2 with positive mean rejects)
- Supporting check: down-bar share on active vs all bars (binomial z): -0.0183191, passed: False
- Counts: active bars: 434, down-cross stretches: 5
- Decided by: Inconclusive: t lies strictly between -2 and +2.
- Reading: Coin mean taken over all tested bars of all windows; t of the weighted mean uses the weighted variance with Kish effective n; a down-cross stretch is a run of bars with negative raw SMA spread containing an active bar; the supporting check passes when z >= 2.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`

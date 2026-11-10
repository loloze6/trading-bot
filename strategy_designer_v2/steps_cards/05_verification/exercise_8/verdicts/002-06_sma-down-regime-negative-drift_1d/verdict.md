---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean next-bar return minus coin mean, on bars with forecast < 0: -0.00100349; t of weighted mean (sandwich SE): -0.533451 (threshold: confirm if negative with t <= -2; reject if positive with t >= +2; else inconclusive)
- Supporting check: binomial z, share of down next bars, active minus all: -0.0183191, passed: False
- Counts: active bars: 434, down-cross stretches: 5
- Decided by: Inconclusive: t lies strictly between -2 and +2.
- Reading: Coin mean is the mean next-bar return pooled over all bars of all windows; the weighted t uses SE = sqrt(sum w^2 (x-m)^2)/sum w * sqrt(n/(n-1)); a stretch is a run of raw SMA spread < 0 inside a window containing at least one forecast < 0 bar; a down bar is a negative next-bar return, and the supporting check passes at z >= 2.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`

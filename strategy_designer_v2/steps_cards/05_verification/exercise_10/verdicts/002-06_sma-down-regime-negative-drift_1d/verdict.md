---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean of next-bar return minus coin mean bar return, on forecast<0 bars: -0.00100349; t of weighted mean: -0.533451 (threshold: confirm if negative with t <= -2; reject if positive with t >= +2; otherwise inconclusive)
- Supporting check: down-bar share on active bars vs all bars (binomial z): -0.0183191, passed: False
- Counts: active bars: 434, down-cross stretches: 5
- Decided by: The t-statistic lies strictly between -2 and +2, meeting the inconclusive rule.
- Reading: The coin's mean bar return is the mean next-bar return over all tested bars pooled across the 6 windows; the t of the weighted mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w); active bars are forecast<0 bars with a valid next return; down-cross stretches are runs of consecutive bars with the raw 50/200 SMA spread below 0 within a window; the raw spread is read from the record's only component column (sma_cross_down) since the config's id sma_spread is absent; the supporting check passes when the binomial z of the down-bar share (active minus all) is above 0.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`

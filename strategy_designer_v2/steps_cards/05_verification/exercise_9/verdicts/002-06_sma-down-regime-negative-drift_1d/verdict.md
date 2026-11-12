---
plan: 002-06_sma-down-regime-negative-drift_1d
idea: 002-06_sma-down-regime-negative-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted next-bar return minus coin mean, on short bars: -0.00100349; t of weighted mean: -0.538966 (threshold: confirm if weighted excess return < 0 with t <= -2; reject if > 0 with t >= +2; otherwise inconclusive)
- Supporting check: down-bar share on active vs all bars (binomial z): -0.0183191, passed: False
- Counts: active bars: 434, down-cross stretches: 5
- Decided by: The t-statistic lies strictly between -2 and +2 (inconclusive rule).
- Reading: The plan's component id 'sma_spread' is read from whichever 'debug_info.components.*.last_history_value' column the record holds (here 'sma_cross_down'), and the situation is a raw spread below 0 with a negative forecast; the coin's mean bar return is pooled over all bars of all windows; the t of the weighted mean uses the weighted standard deviation over the Kish effective sample size; a down bar is a negative next-bar return; the supporting check passes when z >= 2, since the plan gives no threshold of its own; a separate down-cross stretch is a run, within one window, of consecutive bars with raw spread < 0 that holds at least one active bar; missing a minimum count gives 'not observable', as the instructions require.
Plan: `steps_cards/03_test_plan/plans/002-06_sma-down-regime-negative-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-06_sma-down-regime-negative-drift_1d`
Measure: `measure.py`

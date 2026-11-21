---
plan: 005-02_bullish-rsi-divergence-rebound_1d
idea: 005-02_bullish-rsi-divergence-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of x = (forecast/10) x (10-bar return - coin mean 10-bar return): -0.0087686; ordinary t of the mean: -1.35407 (threshold: confirm: mean > 0 with t >= 2 over >= 30 independent cases; reject: mean < 0 with t <= -2 over >= 30)
- Supporting check: mean 10-bar return of divergence cases minus new-low cases with forecast 0: -0.0104443, passed: False
- Counts: independent cases: 78, divergence cases (regime, forecast > 0): 78, new-low cases with forecast 0: 98
- Decided by: t lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: The new-30-day-low situation is recomputed per window as close below the minimum of the prior 30 closes, falling back to the recorded regime ('mean_reversion') on a window's first 30 bars where that cannot be computed; the coin's mean 10-bar return is taken on the non-overlapping grid (positions 0, 10, 20, ... of each window) over all its windows; cases without a close 10 bars ahead in the same window are left out before the non-overlap rule; 'regime bars' are bars with regime 'mean_reversion'; the plan's 'fewer than 30 independent cases' minimum is reported as not observable.
- Size: unusual move -0.92 % per case over 10 bars, -0.037 of the coin's usual move (12.83 %); normal drift in its direction +1.26 %, total +0.34 %; 47 cases
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound_1d`
Measure: `measure.py`

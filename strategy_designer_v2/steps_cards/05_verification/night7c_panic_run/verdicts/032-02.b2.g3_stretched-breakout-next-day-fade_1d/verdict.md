---
plan: 032-02.b2.g3_stretched-breakout-next-day-fade_1d
idea: 032-02.b2.g3_stretched-breakout-next-day-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-bar return on breakout size (-forecast): -0.000394968; day-clustered OLS slope t: -0.609698 (threshold: t <= -2 confirms (with mean unusual short move > 0); t >= +2 rejects; otherwise inconclusive)
- Supporting check: mean unusual move in short direction: -0.00284342, passed: False
- Counts: distinct days with a breakout case: 491, breakout cases: 782
- Decided by: Slope t is between -2 and +2: inconclusive per the plan.
- Reading: All bars with regime 'mean_reversion' and a next bar in the same window are cases, including those with forecast 0 (size 0); the slope's t uses day-clustered (CR1) standard errors from OLS of the drift-removed next-bar return on -forecast; the drift is each coin's mean next-bar return pooled over all its windows; days are UTC calendar days of the bar's timestamp.
- Size: unusual move +0.01 % (t 0.03, the cases of one day together: 256 days) per case over 1 bars, 0.012 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total -0.11 %; 356 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g3_stretched-breakout-next-day-fade_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g3_stretched-breakout-next-day-fade_1d`
Measure: `measure.py`

---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of de-meaned forward 20-bar return on forecast, pooled: 1.22072; OLS slope t: 1.22072 (threshold: confirm if t >= 2 (with positive timing gain); reject if t <= -2)
- Supporting check: book timing gain (mean daily return minus market-rise gain): 0.000416932, passed: True
- Counts: grid cases with forecast above 0: 284, grid cases in total: 827
- Decided by: Minimum counts not reached: 284 grid cases with forecast above 0 (need 100) and 827 cases in total (need about 860).
- Reading: The situation 'close at or above SMA(200)' is read from the recorded regime == 'trending', because the detector's ma200 component is not recorded and windows are too short to recompute a 200-bar SMA, with the expected side long (forecast > 0) and the range position and rise only grading the size; the coin's mean 20-bar return is the mean of its non-overlapping grid returns over all windows, the slope t is the OLS slope t (with intercept) of the pooled grid cases, 'about 860 cases' is taken as at least 860 grid cases, and the book's daily returns are postRebalance_total_value bar-to-bar within each window, averaged across coins per day.
- Size: unusual move +2.44 % per case over 20 bars, 0.075 of the coin's usual move (21.24 %); normal drift in its direction +2.45 %, total +4.89 %; 406 cases
Plan: `steps_cards/03_test_plan/hold_paying_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d.md`
Record: `steps_cards/04_backtest/hold_paying_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d`
Measure: `measure.py`

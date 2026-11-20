---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 336-bar excess return on forecast, pooled, trending grid bars: 0.00265407; OLS slope t: 2.18127 (threshold: confirm if t >= 2 (with positive timing part); reject if t <= -2)
- Supporting check: timing part of book daily returns: -0.00197481, passed: False
- Counts: grid cases in the regime: 576, grid cases in the regime with a forecast above 0: 361
- Decided by: The slope's t is 2 or more but the timing part is not positive.
- Reading: The regression uses all trending grid bars (forecast zero included) with an intercept, each coin's mean 336-bar return is taken over the non-overlapping grids of all its windows, the regime is the recorded 'regime' column, and the daily position held is the mean allocation over the bars spanning each day's return.
- Size: unusual move +0.03 % per case over 336 bars, 0.002 of the coin's usual move (17.69 %); normal drift in its direction +2.04 %, total +2.07 %; 1126 cases
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h`
Measure: `measure.py`

---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 10-bar forward return on forecast, trending grid bars: 0.00339149; OLS slope t: 4.19135 (threshold: t >= 2 confirms (with timing gain > 0), t <= -2 rejects)
- Supporting check: book timing gain (mean daily return minus market part), before costs: 0.000344534, passed: True
- Counts: trending grid cases: 833
- Decided by: The slope's t is 2 or more and the timing gain is above 0 before costs.
- Reading: The 200-day condition is read from the recorded regime 'trending' (the detector's components are not recorded and the windows are too short to recompute a 200-day average), the situation is a trending bar with the vsr component recorded (graded, so any size counts) on the long side; the coin's mean 10-bar return is the mean over all grid bars of all its windows, the slope is an OLS slope with intercept, and the book's daily return is postRebalance_total_value bar to bar inside a window with the market part from the position held into that day.
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d`
Measure: `measure.py`

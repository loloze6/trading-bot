---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on positive forecast, pooled: 0.0010011; OLS slope t: 2.37024 (threshold: confirm if slope t >= 2 with supporting check passing; reject if slope t <= -2)
- Supporting check: top fifth minus bottom fifth mean 5-bar excess return > 0: 0.0138147, passed: True
- Counts: independent positive-forecast cases: 1660, top fifth cases: 332, bottom fifth cases: 332
- Decided by: Slope t >= 2 and the top-minus-bottom fifth excess return difference is > 0.
- Reading: Coin mean 5-bar return is taken over all grid bars of all its windows; the top and bottom fifths are the n//5 largest and n//5 smallest positive forecasts by stable sort of the pooled grid cases; the plan's 300-case minimum maps to 'not observable'; the situation's up day is read from the close-to-close return (raw component sign on a window's first row).
- Size: unusual move -0.25 % per case over 5 bars, -0.026 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.34 %; 3175 cases
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d`
Measure: `measure.py`

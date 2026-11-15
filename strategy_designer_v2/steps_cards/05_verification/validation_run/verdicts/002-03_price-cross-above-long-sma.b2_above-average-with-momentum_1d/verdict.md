---
plan: 002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d
idea: 002-03_price-cross-above-long-sma.b2_above-average-with-momentum
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 20-bar return on forecast (active non-overlapping cases): 0.00784211; OLS slope t: 1.646 (threshold: slope t >= 2 confirms (with supporting check), slope t <= -2 rejects)
- Supporting check: forecast-weighted mean excess 20-bar return > 0: 0.0300932, passed: True
- Counts: active non-overlapping cases: 254
- Decided by: Inconclusive: slope t = 1.65 and weighted-mean t = 0.86 meet neither the confirm nor the reject rule.
- Reading: Coin's mean 20-bar return taken over all non-overlapping grid cases of all its windows; slope t is the OLS t of excess return on forecast; the forecast-weighted mean's t is the ordinary t of the mean of forecast x excess; fewer than 30 active cases is reported as not observable.
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d`
Measure: `measure.py`

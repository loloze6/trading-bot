---
plan: N1-08_twenty-day-momentum_1d
idea: N1-08_twenty-day-momentum
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-statistic of slope of forward 20-bar excess return on forecast (non-overlapping, pooled): 0.0587466; OLS slope t: 0.0587466 (threshold: confirm if t >= 2 and top-minus-bottom > 0; reject if t <= -2; otherwise inconclusive)
- Supporting check: mean forward 20-bar excess return, top fifth minus bottom fifth of forecasts: -0.0165032, passed: False
- Counts: non-overlapping 20-bar cases: 827
- Decided by: The slope t-statistic lies between -2 and 2.
- Reading: Each coin's mean 20-bar return is taken over all bars of all its windows that have a forward return. The regression and the top/bottom fifths (cut at the 80th and 20th percentiles of forecasts) both use the same pooled non-overlapping sample at positions 0, 20, 40, ... of each window, and too few cases is reported as not observable.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N1-08_twenty-day-momentum_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-08_twenty-day-momentum_1d`
Measure: `measure.py`

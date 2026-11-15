---
plan: 002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum_1d
idea: 002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 20-bar forward return on active non-overlapping cases: 0.0164929; ordinary t of the mean: 0.533758 (threshold: t >= 2.0 confirms (with slope > 0), t <= -2.0 rejects, over at least 30 active cases)
- Supporting check: OLS slope of excess 20-bar forward return on forecast: 0.00085788, passed: True
- Counts: active non-overlapping cases: 329, active bars: 6890
- Decided by: t is between -2.0 and 2.0, which the plan calls inconclusive.
- Reading: The situation is checked as regime == 'trending' (the detector's close-above-200-SMA rule) and ret60 last_history_value > 0 with a positive forecast; the coin's mean 20-bar return is the mean over all windows' non-overlapping grid bars (positions 0, 20, 40, ...), active or not, and a case is a grid bar with forecast > 0 and a forward return inside its window.
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum_1d`
Measure: `measure.py`

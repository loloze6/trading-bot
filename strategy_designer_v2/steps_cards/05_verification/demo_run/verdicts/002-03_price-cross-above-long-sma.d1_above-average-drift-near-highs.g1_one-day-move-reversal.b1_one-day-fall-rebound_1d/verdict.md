---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of position x next-day excess return on forecast > 0 bars: 0.00110178; t of the mean: 3.9154 (threshold: t >= 2 (with supporting check) to confirm, t <= -2 to reject, at least 100 positive-forecast bars)
- Supporting check: top minus bottom forecast quintile mean next-day excess return > 0: 0.00471156, passed: True
- Counts: positive-forecast bars: 8514, top quintile bars: 1703, bottom quintile bars: 1703
- Decided by: t >= 2 with at least 100 positive-forecast bars and the top-minus-bottom quintile excess return > 0.
- Reading: A bar is in the situation when the coin's one-day return close[t]/close[t-1]-1 inside the window is negative (on a window's first bar, when the raw 'fall' component value is negative), the expected side is long; the 100-bar minimum counts positive-forecast bars with a next-day return in the same window; the coin's mean daily return is the mean of all its next-day returns over all windows; quintiles are forecast >= 80th and <= 20th percentile of the positive forecasts (ties included).
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound_1d`
Measure: `measure.py`

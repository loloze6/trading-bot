---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 10-bar return minus coin mean on forecast, trending bars: 0.000361233; OLS slope t: 0.908929 (threshold: t >= 2 confirms (with timing gain > 0), t <= -2 rejects, with at least 100 independent cases)
- Supporting check: timing gain (book mean daily return minus market-rise gain), before costs: -0.000297672, passed: False
- Counts: independent cases: 833
- Decided by: The slope's t is between -2 and 2.
- Reading: Trending bars are those with regime 'trending' at grid positions 0,10,20,... of each window with a full 10-bar forward return inside the window; the coin's mean 10-bar return is the mean over the same non-overlapping grid of all bars in all windows; the slope's t is the OLS t with an intercept on pooled coins; the side check uses the sign of range20 - 0.5*ext30 on trending bars.
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d`
Measure: `measure.py`

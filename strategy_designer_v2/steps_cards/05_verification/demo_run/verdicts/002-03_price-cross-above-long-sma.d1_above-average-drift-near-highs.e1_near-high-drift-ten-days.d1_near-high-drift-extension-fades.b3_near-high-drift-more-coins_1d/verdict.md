---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-excess 10-bar forward return on forecast, trending-regime grid bars: 0.00144688; OLS slope t: 1.31205 (threshold: slope t >= +2 confirms (with check), t <= -2 rejects; at least 100 independent cases)
- Supporting check: slope of excess 10-bar return on raw 30-day return, grid bars with ext30 post value <= -5: -8.49021e-07, passed: True
- Counts: trending-regime grid cases: 1547, extended cases: 513
- Decided by: Main slope t lies between -2 and +2.
- Reading: Situation taken as the 'trending' regime (close >= 200-day SMA, which cannot be recomputed from windows shorter than 200 bars) with the expected side the sign of the graded idea (mean of range20 and ext30 post values, ext30 never positive); the coin's mean 10-bar return is the mean over all its grid bars in all windows and regimes; regressions are OLS with intercept; the 100 trending grid cases is treated as the plan's minimum count, while the 30 extended cases is part of the supporting check as the plan writes it (fewer gives inconclusive).
- Size: unusual move +0.62 % per case over 10 bars, 0.030 of the coin's usual move (16.13 %); normal drift in its direction -0.43 %, total +0.20 %; 1625 cases
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d`
Measure: `measure.py`

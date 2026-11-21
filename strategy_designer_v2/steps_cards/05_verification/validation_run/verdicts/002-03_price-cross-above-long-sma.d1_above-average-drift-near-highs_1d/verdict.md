---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (next 20-bar return minus coin's mean 20-bar return) on grid bars with forecast > 0: 0.0195146; t of the mean: 0.606872 (threshold: mean > 0 with t >= 2 to confirm, mean < 0 with t <= -2 to reject, on at least 100 cases)
- Supporting check: book Calmar minus holding Calmar (before costs), passes if >= 0: 0.763891, passed: True
- Counts: grid cases with a positive forecast: 284, active bars: 6128
- Decided by: The t lies between -2 and 2 (or is undefined), meeting neither the confirm nor the reject rule.
- Reading: Situation checked on regime == 'trending' with forecast > 0; grid bars are positions 0, 20, 40, ... of each window that have a bar 20 ahead in the same window; the coin's mean 20-bar return is the mean over all its grid samples in all windows; the book is postRebalance_total_value per bar, coins averaged per day, chained over windows w1..wN in order, and holding is the same from closes.
- Size: unusual move +2.44 % per case over 20 bars, 0.075 of the coin's usual move (21.24 %); normal drift in its direction +2.45 %, total +4.89 %; 406 cases
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d`
Measure: `measure.py`

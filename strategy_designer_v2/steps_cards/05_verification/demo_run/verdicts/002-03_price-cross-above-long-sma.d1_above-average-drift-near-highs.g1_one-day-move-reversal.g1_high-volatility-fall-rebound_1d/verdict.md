---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-bar return minus coin mean on forecast, mean_reversion bars, pooled: 0.00110273; OLS slope t: 5.88639 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive)
- Supporting check: slope(pct>=0.9) minus slope(0.8<=pct<0.9) among forecast>0 bars: -0.000433918, passed: False
- Counts: bars with forecast > 0 in the regime: 1698, regime bars in regression: 3447, forecast>0 bars with percentile >= 0.9: 636, forecast>0 bars with percentile 0.8-0.9: 242, active bars: 1708
- Decided by: The slope's t is >= 2 but the supporting check fails, which the plan calls inconclusive.
- Reading: The fall is read as the recorded raw VolatilityScaledReturn (last_history_value) below 0 and the regime as the recorded 'mean_reversion' label; the main regression uses every mean_reversion bar (forecast 0 included) with an OLS slope t; the supporting check's percentile is recomputed inside each window as the rank of the 20-bar return std among its last up-to-100 values (at least 20), smoothed over 5 bars as in the config, and compares OLS slopes of next-bar return on forecast among forecast>0 bars (>=0.9 minus 0.8-0.9); the 100-bar minimum is applied as a minimum count giving 'not observable'.
- Size: unusual move +0.63 % per case over 1 bars, 0.130 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.75 %; 1115 cases
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d`
Measure: `measure.py`

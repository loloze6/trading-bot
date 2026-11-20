---
plan: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends_1d
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 10-bar forward return on recorded 20-bar return, in-regime grid bars: 0.000147791; OLS slope t: 1.69221 (threshold: confirm if slope t >= 2 and supporting difference > 0; reject if slope t <= -2)
- Supporting check: mean excess 10-bar return, positive-forecast minus zero-forecast cases: 0.0319364, passed: True
- Counts: independent in-regime cases: 853, cases with positive forecast: 426, cases with zero forecast: 427
- Decided by: The slope t lies between -2 and 2.
- Reading: Spread above 0 is read from the regime column being 'trending'. The coin's mean 10-bar return is taken over all grid bars of all its windows. The regressor is the raw mom20 last_history_value, and the forecast groups use the forecast on the same grid bars.
- Size: unusual move +1.24 % per case over 10 bars, 0.070 of the coin's usual move (14.49 %); normal drift in its direction +1.16 %, total +2.40 %; 506 cases
Plan: `steps_cards/03_test_plan/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends_1d`
Measure: `measure.py`

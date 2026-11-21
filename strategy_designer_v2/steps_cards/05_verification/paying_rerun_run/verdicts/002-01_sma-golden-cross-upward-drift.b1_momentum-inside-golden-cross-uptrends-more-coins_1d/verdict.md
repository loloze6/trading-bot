---
plan: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 10-bar return on forecast (trending grid bars): 0.00216422; OLS slope t: 4.61258 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects)
- Supporting check: mean excess return top third minus bottom third of forecasts: 0.0617564, passed: True
- Counts: independent trending cases: 1592, cases per third: 530
- Decided by: The slope is above 0 with t >= 2 and the top-minus-bottom-third excess return is above 0.
- Reading: Situation read on the `regime` column (SMA50>SMA200 = `trending`), and an active bar is on the expected side when its forecast sign matches the 20-day return or that return minus its trailing 60-value mean (the standardisation may demean); the regression is OLS with intercept on all trending grid bars, the coin's mean 10-bar return is taken over the non-overlapping grid bars of all its windows, and thirds are the lowest and highest floor(n/3) cases sorted by forecast.
- Size: unusual move +1.83 % per case over 10 bars, 0.103 of the coin's usual move (16.13 %); normal drift in its direction -0.02 %, total +1.81 %; 1487 cases
Plan: `steps_cards/03_test_plan/validation_run/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d`
Measure: `measure.py`

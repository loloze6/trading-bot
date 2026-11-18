---
plan: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 10-bar return on forecast (trending grid bars): 0.00114958; OLS slope t: 0.675255 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects)
- Supporting check: mean excess return top third minus bottom third of forecasts: 0.00958633, passed: True
- Counts: independent trending cases: 193, cases per third: 64
- Decided by: The slope's t lies between -2 and 2.
- Reading: Situation read on the `regime` column (SMA50>SMA200 = `trending`), and an active bar is on the expected side when its forecast sign matches the 20-day return or that return minus its trailing 60-value mean (the standardisation may demean); the regression is OLS with intercept on all trending grid bars, the coin's mean 10-bar return is taken over the non-overlapping grid bars of all its windows, and thirds are the lowest and highest floor(n/3) cases sorted by forecast.
Plan: `steps_cards/03_test_plan/validation_run/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d.md`
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d`
Measure: `measure.py`

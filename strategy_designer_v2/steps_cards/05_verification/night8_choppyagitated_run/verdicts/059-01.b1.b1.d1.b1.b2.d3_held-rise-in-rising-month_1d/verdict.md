---
plan: 059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month_1d
idea: 059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess forward 7-bar return on forecast (grid bars, forecast > 0): 0.000306781; slope t: 0.15235 (threshold: confirm: slope t >= 2 (with weighted mean > 0, t >= 2); reject: slope t <= -2 or weighted mean t <= -2; at least 30 cases)
- Supporting check: forecast-weighted mean excess forward 7-bar return (t): 0.0194035, passed: False
- Counts: cases: 108
- Decided by: Inconclusive rule: neither the confirm nor the reject rule is met by the slope's t and the weighted mean's t, over at least 30 cases.
- Reading: Situation rebuilt as: recorded scaled_rise raw value > 0, close in the top 20 % of the 7-bar high-low range (current bar included) and close/close[-30]-1 > 0, long side, using the recorded regime 'trending' where a window's first bars cannot rebuild those inputs; the coin's mean 7-bar return is taken over its 0,7,14,... grid of all windows; the slope's t is the OLS slope over its standard error; the weighted mean's t uses the standard error sqrt(sum w^2 (x-m)^2)/sum w.
- Size: unusual move +1.30 % (t 1.41, the cases of one day together: 231 days) per case over 7 bars, 0.096 of the coin's usual move (12.84 %); normal drift in its direction +0.94 %, total +2.24 %; 344 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b2.d3_held-rise-in-rising-month_1d`
Measure: `measure.py`

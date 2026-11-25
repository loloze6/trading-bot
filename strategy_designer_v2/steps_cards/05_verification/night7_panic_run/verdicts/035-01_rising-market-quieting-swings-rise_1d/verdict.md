---
plan: 035-01_rising-market-quieting-swings-rise_1d
idea: 035-01_rising-market-quieting-swings-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 3-bar return over positive-forecast grid bars: 0.00244267; t of the weighted mean, cases of one day pooled: 0.605151 (threshold: confirm: positive with t >= 2 (and supporting difference > 0); reject: negative with t <= -2)
- Supporting check: mean excess 3-bar return, forecast above median of positive forecasts minus forecast 0, inside rising profile: 0.00406232, passed: True
- Counts: positive-forecast grid cases: 1209, distinct days: 522, supporting group above median: 604, supporting group forecast 0: 1015
- Decided by: The t of the main measure lies between -2 and 2.
- Reading: The rising profile is the recorded regime 'unknown' (not the chop veto), the coin's mean is over its grid 3-bar returns of all windows, the t pools each day's weighted deviations into one cluster (SE^2 = sum of squared day sums / (sum of weights)^2 x G/(G-1)), the median is over positive-forecast grid bars inside the profile, and a missing supporting group counts as a failed check.
- Size: unusual move +0.53 % (t 1.20, the cases of one day together: 475 days) per case over 3 bars, 0.071 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.89 %; 673 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/035-01_rising-market-quieting-swings-rise_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/035-01_rising-market-quieting-swings-rise_1d`
Measure: `measure.py`

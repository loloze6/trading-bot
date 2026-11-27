---
plan: 077-01_agitated-high-close-week-rise_1d
idea: 077-01_agitated-high-close-week-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 7-bar return: 0.00281163; t of weighted mean, same-day cases together: 0.300872 (threshold: weighted mean > 0 with t >= 2 to confirm; < 0 with t <= -2 to reject)
- Supporting check: top third minus bottom third mean excess return: 0.0253794, passed: True
- Counts: independent grid cases with forecast > 0: 1138, days the cases fall on: 277
- Decided by: t between -2 and 2 (or undefined): inconclusive.
- Reading: Cases are grid bars (positions 0, 7, 14, ... of each window) with forecast > 0 and a full 7-bar forward return; the coin mean is over all its grid returns in all windows; t uses day-clustered deviations of the weighted mean; terciles are the n//3 highest and lowest forecasts, unweighted means; fewer than 100 cases is reported as not observable.
- Size: unusual move -0.00 % (t -0.01, the cases of one day together: 824 days) per case over 7 bars, 0.001 of the coin's usual move (12.84 %); normal drift in its direction +1.01 %, total +1.01 %; 2228 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/077-01_agitated-high-close-week-rise_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/077-01_agitated-high-close-week-rise_1d`
Measure: `measure.py`

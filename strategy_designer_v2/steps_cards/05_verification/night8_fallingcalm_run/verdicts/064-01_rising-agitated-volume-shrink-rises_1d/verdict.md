---
plan: 064-01_rising-agitated-volume-shrink-rises_1d
idea: 064-01_rising-agitated-volume-shrink-rises
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the excess 5-day return on the forecast, profile grid bars: 1.57796; OLS slope t: 1.57796 (threshold: confirm if t >= +2 and check mean > 0; reject if t <= -2; inconclusive otherwise)
- Supporting check: mean excess 5-day return on grid bars with forecast > 0: 0.0129027, passed: True
- Counts: non-overlapping grid cases with forecast > 0: 211, profile grid bars in total: 718
- Decided by: The slope's t is between -2 and +2.
- Reading: The profile is the detector's 'unknown' regime on the grid bar, the grid is positions 0,5,10,... of each window, all coins are pooled in one regression, and the coin's mean 5-day return is taken over the non-overlapping grid returns of all its windows.
- Size: unusual move +1.71 % (t 1.39, the cases of one day together: 158 days) per case over 5 bars, 0.161 of the coin's usual move (10.60 %); normal drift in its direction +0.63 %, total +2.34 %; 192 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/064-01_rising-agitated-volume-shrink-rises_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/064-01_rising-agitated-volume-shrink-rises_1d`
Measure: `measure.py`

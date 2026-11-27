---
plan: 074-01_rising-calm-wide-low-close-rebound_1d
idea: 074-01_rising-calm-wide-low-close-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day return minus coin's mean daily return, forecast > 0 cases, before costs: 0.00634202; t of the mean, pooled by day: 1.92506 (threshold: mean > 0 with t >= 2 confirms; t <= -2 rejects; |t| < 2 inconclusive)
- Supporting check: correlation between forecast and next-day excess return: 0.0999003, passed: True
- Counts: distinct case days: 225, cases: 426, active bars: 427
- Decided by: Inconclusive: |t| of the mean excess next-day return is below 2.
- Reading: The rising-calm profile is taken from the recorded regime (its 365-bar volatility percentile and 60-bar trend cannot be rebuilt inside the windows) while width and nearness to the low are recomputed from prices; the day-pooled t is the mean excess per case over its standard error clustered by UTC day (deviations summed per day), and the correlation's t is r*sqrt((n-2)/(1-r^2)) over all cases.
- Size: unusual move +0.67 % (t 2.00, the cases of one day together: 215 days) per case over 1 bars, 0.140 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.81 %; 404 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/074-01_rising-calm-wide-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01_rising-calm-wide-low-close-rebound_1d`
Measure: `measure.py`

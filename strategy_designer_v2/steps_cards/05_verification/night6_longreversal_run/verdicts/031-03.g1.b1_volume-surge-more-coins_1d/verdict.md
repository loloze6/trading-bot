---
plan: 031-03.g1.b1_volume-surge-more-coins_1d
idea: 031-03.g1.b1_volume-surge-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (14-bar forward return - coin's mean 14-bar return), grid cases: 0.0231811; t of the mean, cases summed per day: 2.34169 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean directional excess 14-bar return, |forecast| above median minus below: 0.0199905, passed: True
- Counts: cases: 2448, distinct days: 207
- Decided by: the main mean is positive with t >= 2 and the supporting check passes
- Reading: Every grid bar (positions 0,14,28,... per coin and window) with a 14-bar forward return inside its window is a case, forecast 0 included; the coin's mean 14-bar return is the mean over its grid cases of all windows; the t clusters case deviations summed per UTC day (with D/(D-1) correction); the median split uses |forecast| strictly above vs strictly below the median, directional excess = sign(forecast) x excess return.
- Size: unusual move +0.66 % (t 1.02, the cases of one day together: 1056 days) per case over 14 bars, 0.026 of the coin's usual move (20.98 %); normal drift in its direction -0.19 %, total +0.47 %; 2274 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1_volume-surge-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1_volume-surge-more-coins_1d`
Measure: `measure.py`

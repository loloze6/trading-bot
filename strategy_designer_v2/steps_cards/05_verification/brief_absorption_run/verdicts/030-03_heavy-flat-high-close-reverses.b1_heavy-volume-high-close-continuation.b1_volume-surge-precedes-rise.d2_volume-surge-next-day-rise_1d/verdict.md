---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-statistic of pooled OLS slope of next-day excess return on forecast: 4.70191; OLS slope t: 4.70191 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 bars with forecast > 0)
- Supporting check: none
- Counts: bars with a forecast above 0: 6703, bars in the fit: 17380
- Decided by: Confirm rule: the slope is positive with t >= 2, on at least 300 bars with a forecast above 0.
- Reading: Every bar with a next-day close in the same window enters the fit (zero-forecast bars included), the coin's mean daily return is the mean of all its in-window next-day returns, and the t is the ordinary OLS slope t with an intercept; the situation is a raw centred volume ratio above 0 with a positive forecast.
- Size: unusual move +0.09 % per case over 1 bars, 0.017 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.21 %; 3620 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d`
Measure: `measure.py`

---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-bar excess return on forecast: 0.000185556; OLS slope t: 3.30067 (threshold: confirm: t >= 2 with mean excess return on forecast > 0 bars above 0; reject: t <= -2)
- Supporting check: mean next-bar excess return on forecast > 0 bars: 0.00149427, passed: True
- Counts: bars: 17380, bars with forecast > 0: 4246
- Decided by: The slope has t >= 2 and the mean excess return on forecast > 0 bars is above 0.
- Reading: The slope is an ordinary least-squares regression over every bar with a next bar in its window (horizon 1, so every bar is its own grid cell), the coin mean is the mean of all its next-bar returns over all windows, and the plan's 'fewer than 100 forecast > 0 bars' minimum is treated as 'not observable' as the workflow requires.
- Size: unusual move +0.15 % per case over 1 bars, 0.033 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.27 %; 2558 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d`
Measure: `measure.py`

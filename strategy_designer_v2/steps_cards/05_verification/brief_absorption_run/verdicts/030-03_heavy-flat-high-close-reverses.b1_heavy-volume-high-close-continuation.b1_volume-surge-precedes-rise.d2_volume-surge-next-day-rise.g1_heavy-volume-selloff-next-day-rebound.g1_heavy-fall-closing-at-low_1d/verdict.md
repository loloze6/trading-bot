---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of next-day excess return on forecast, down days with forecast > 0: 4.16027; OLS slope t: 4.16027 (threshold: t >= 2 (with top-fifth mean > 0) confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: top-fifth down-day mean next-day excess return: 0.00295406, passed: True
- Counts: down-day bars with a forecast above 0: 8470, down-day bars: 8473, top-fifth down-day bars: 1695
- Decided by: The slope's t is 2 or more and the top-fifth mean excess return is above 0 (confirm rule).
- Reading: Down day = close below the previous close within the same window (a window's first bar has no prior close and is not a down day); the regression pools every down-day bar with forecast > 0 and a next close in its window across all coins and windows, OLS slope t = slope / its standard error; the coin's mean daily return is the mean of all its in-window 1-day returns; the top fifth is the ceil(20 %) highest-forecast down-day bars (any forecast, ties by record order) pooled across coins; the plan's 200-case minimum gives 'not observable'.
- Size: unusual move +0.17 % per case over 1 bars, 0.037 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.29 %; 5478 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d`
Measure: `measure.py`

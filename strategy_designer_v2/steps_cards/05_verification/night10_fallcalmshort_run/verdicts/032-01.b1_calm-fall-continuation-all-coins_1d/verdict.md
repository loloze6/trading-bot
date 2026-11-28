---
plan: 032-01.b1_calm-fall-continuation-all-coins_1d
idea: 032-01.b1_calm-fall-continuation-all-coins
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean daily timing gain on bars in a position (position x (next-day return - coin drift), summed per day): 0.00101714; t of the mean over days: 0.557904 (threshold: t >= 2 confirm, t <= -2 reject, over at least 100 days in a position)
- Supporting check: deeper-half minus shallower-half next-day excess return: -0.000656493, passed: True
- Counts: days in a position: 979, bars in a position: 2062, deeper half bars: 1031, shallower half bars: 1031
- Decided by: Timing gain t lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.558 (below 1), 979 cases (30 needed).
- Reading: The falling calm profile is read from the recorded regime ('unknown' = no veto fired, since the detector's components are not recorded and the 365-bar volatility percentile cannot be rebuilt inside a window), the situation is that profile with the 30-day change below 0 on the short side; bars in a position are those with a nonzero position after the trade; the drift is the coin's mean one-bar return over all its windows; the supporting split uses position bars with a negative forecast, deeper half = forecast at or below the median; fewer than 100 days in a position is treated as the plan's minimum count, so 'not observable'.
- Size: unusual move +0.01 % (t 0.04, the cases of one day together: 426 days) per case over 1 bars, 0.003 of the coin's usual move (4.55 %); normal drift in its direction -0.09 %, total -0.08 %; 643 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.558 (below 1), 979 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/032-01.b1_calm-fall-continuation-all-coins_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/032-01.b1_calm-fall-continuation-all-coins_1d`
Measure: `measure.py`

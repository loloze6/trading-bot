---
plan: 061-01_falling-calm-scaled-rise-fade_1d
idea: 061-01_falling-calm-scaled-rise-fade
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain: position x (next-day return - coin mean daily return): -0.00163353; t of the mean, day-clustered: -1.44168 (threshold: confirm: mean > 0 with t >= 2 (and slope check passes); reject: mean < 0 with t <= -2)
- Supporting check: slope of next-day excess return on forecast (forecast < 0), day-clustered t >= 2: -1.35314, passed: False
- Counts: distinct days with a nonzero position: 607, position bars with next-day return: 1164, days of position cases: 607, forecast-below-0 bars in regression: 1461, days in regression: 722
- Decided by: Main t between -2 and 2: inconclusive. No effect (common/verdicts.md): t in the idea's direction -1.442 (below 1), 607 cases (30 needed).
- Reading: The falling calm profile is read from the recorded regime ('unknown' = neither veto fired), an up day from the raw scaled rise > 0; a nonzero position is postRebalance_current_allocation != 0; 'cases of one day summed together' is read as day-clustered standard errors (deviations / scores summed per day) for both the mean and the slope; the 100-day minimum counts all bars with a nonzero position.
- Size: unusual move -0.25 % (t -1.45, the cases of one day together: 478 days) per case over 1 bars, -0.050 of the coin's usual move (4.83 %); normal drift in its direction -0.05 %, total -0.31 %; 845 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -1.442 (below 1), 607 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/061-01_falling-calm-scaled-rise-fade_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/061-01_falling-calm-scaled-rise-fade_1d`
Measure: `measure.py`

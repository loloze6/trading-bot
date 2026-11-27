---
plan: 032-01.b1_calm-fall-continuation-all-coins_1d
idea: 032-01.b1_calm-fall-continuation-all-coins
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on |forecast|: -6.33781e-06; day-clustered OLS slope t: -0.030573 (threshold: confirm: slope < 0 with t <= -2 and mean short-direction excess return > 0; reject: slope > 0 with t >= +2; inconclusive otherwise; minimum 300 cases on at least 100 distinct days)
- Supporting check: mean short-direction next-day excess return > 0: -0.000758124, passed: False
- Counts: cases: 2502, distinct days: 1076
- Decided by: The slope's |t| is below 2, meeting neither the confirm nor the reject rule. No effect (common/verdicts.md): t in the idea's direction +0.031 (below 1), 2502 cases (30 needed).
- Reading: The falling calm profile is read from the recorded `regime` column (the detector's non-vetoed regime 'unknown'), the 30-day fall from fall30's raw value (recomputed from closes inside the window if missing), the coin's mean daily return is the mean of all its in-window next-day returns over all windows, and the slope's t is an OLS slope with day-clustered standard errors (CR1 factor G/(G-1)).
- Size: unusual move -0.17 % (t -0.72, the cases of one day together: 438 days) per case over 1 bars, -0.030 of the coin's usual move (4.83 %); normal drift in its direction -0.05 %, total -0.22 %; 707 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.031 (below 1), 2502 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/032-01.b1_calm-fall-continuation-all-coins_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/032-01.b1_calm-fall-continuation-all-coins_1d`
Measure: `measure.py`

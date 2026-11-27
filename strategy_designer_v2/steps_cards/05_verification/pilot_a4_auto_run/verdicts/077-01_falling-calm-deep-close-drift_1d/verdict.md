---
plan: 077-01_falling-calm-deep-close-drift_1d
idea: 077-01_falling-calm-deep-close-drift
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-excess 3-bar forward return on forecast (before costs): 0.000252315; OLS slope t: 0.607859 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 3-bar return of deepest third minus shallowest third (< 0 passes): -0.00250927, passed: True
- Counts: independent cases: 1045, active bars: 3222, cases per third: 348
- Decided by: The slope has |t| < 2. No effect (common/verdicts.md): t in the idea's direction +0.608 (below 1), 348 cases (30 needed).
- Reading: The profile is read from the recorded regime ("unknown" = not vetoed) and the depth from its raw value; cases are grid bars 0,3,6,... of each window with a non-zero forecast and a full 3-bar return in the window, the coin's mean is over all its grid bars in all windows, and the thirds are the floor(n/3) most negative and floor(n/3) least negative forecasts.
- Size: unusual move -0.10 % (t -0.28, the cases of one day together: 470 days) per case over 3 bars, -0.010 of the coin's usual move (8.29 %); normal drift in its direction -0.19 %, total -0.29 %; 740 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.608 (below 1), 348 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/077-01_falling-calm-deep-close-drift_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/077-01_falling-calm-deep-close-drift_1d`
Measure: `measure.py`

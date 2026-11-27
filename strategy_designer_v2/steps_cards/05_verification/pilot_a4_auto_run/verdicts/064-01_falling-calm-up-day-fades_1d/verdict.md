---
plan: 064-01_falling-calm-up-day-fades_1d
idea: 064-01_falling-calm-up-day-fades
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 3-bar excess return on forecast (forecast < 0 grid cases): 0.000228104; OLS slope t: 0.451945 (threshold: slope > 0 with t >= 2 confirms; t <= -2 rejects)
- Supporting check: mean unusual move in short direction, day-clustered t (t = -1.448): -0.00693196, passed: False
- Counts: grid cases with forecast < 0: 483, distinct days: 242
- Decided by: Neither the confirm nor the reject rule is met (t values between -2 and 2), so it is inconclusive. No effect (common/verdicts.md): t in the idea's direction +0.452 (below 1), 483 cases (30 needed).
- Reading: The falling-calm profile is read from the recorded regime ('unknown' = no veto, since the detector's components are not recorded), an up day is a positive raw scaled return (or a positive close-to-close return where it is not recorded), all coins in the record are used, the coin's mean 3-bar return is the mean over the non-overlapping grids of all its windows, the day-clustered t sums each day's deviations from the mean, and the plan's 'below the minimum counts it is inconclusive' is reported as 'not observable' as the workflow requires.
- Size: unusual move -0.22 % (t -0.62, the cases of one day together: 465 days) per case over 3 bars, -0.025 of the coin's usual move (8.29 %); normal drift in its direction -0.18 %, total -0.40 %; 817 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.452 (below 1), 483 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/064-01_falling-calm-up-day-fades_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/064-01_falling-calm-up-day-fades_1d`
Measure: `measure.py`

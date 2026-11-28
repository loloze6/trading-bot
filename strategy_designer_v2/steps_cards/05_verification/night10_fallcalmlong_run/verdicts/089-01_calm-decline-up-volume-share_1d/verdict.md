---
plan: 089-01_calm-decline-up-volume-share_1d
idea: 089-01_calm-decline-up-volume-share
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 5-bar forward return on forecast (in-profile grid bars): -0.000682988; OLS t of slope: -1.14311 (threshold: confirm if slope t >= 2 and cases' mean unusual move > 0; reject if slope t <= -2; else inconclusive)
- Supporting check: mean unusual 5-bar move over long-side cases (day-clustered t -1.31): -0.00657727, passed: False
- Counts: in-profile grid bars: 699, in-profile grid bars with forecast above 0: 272, cases: 377, case days: 306
- Decided by: Inconclusive: slope t -1.14 lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -1.143 (below 1), 306 cases (30 needed).
- Reading: In-profile means regime 'unknown' (not vetoed to chop); grid bars count only where the 5-bar forward return exists inside the window; the drift is the coin's mean 5-bar return on the grid of all its windows; cases are long-side forecast rises of >= 2 points from the lowest level since the last bet (reset at flat), first per grid cell; the plan's 'too few -> inconclusive' is reported as 'not observable'.
- Size: unusual move -0.66 % (t -1.31, the cases of one day together: 306 days) per case over 5 bars, -0.053 of the coin's usual move (11.31 %); normal drift in its direction +0.64 %, total -0.02 %; 377 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -1.143 (below 1), 306 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/089-01_calm-decline-up-volume-share_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/089-01_calm-decline-up-volume-share_1d`
Measure: `measure.py`

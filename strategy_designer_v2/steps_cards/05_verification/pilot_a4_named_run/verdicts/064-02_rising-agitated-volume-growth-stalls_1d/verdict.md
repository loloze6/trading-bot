---
plan: 064-02_rising-agitated-volume-growth-stalls_1d
idea: 064-02_rising-agitated-volume-growth-stalls
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar forward return minus normal drift on the forecast: -0.000636049; t of the slope, day-clustered: -0.625783 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases: 484, distinct days: 252
- Decided by: The t of the slope (-0.63) lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -0.626 (below 1), 484 cases (30 needed).
- Reading: The profile (rising agitated) is read from the recorded regime 'unknown' (the only regime with a strategy, the detector's vetoes sending the rest to 'chop'); the expected side is graded, i.e. the forecast's sign opposite to the raw log volume ratio (long on shrinkage, short on growth); the slope is the OLS slope (with intercept) of the excess 5-bar return on the forecast over the active grid cases, and its t uses standard errors clustered by UTC day, so cases on the same day are summed into one piece of evidence; the normal drift is each coin's mean 5-bar return over the non-overlapping grids of all its windows.
- Size: unusual move +0.67 % (t 0.62, the cases of one day together: 266 days) per case over 5 bars, 0.042 of the coin's usual move (11.89 %); normal drift in its direction -0.20 %, total +0.47 %; 308 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.626 (below 1), 484 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/064-02_rising-agitated-volume-growth-stalls_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/064-02_rising-agitated-volume-growth-stalls_1d`
Measure: `measure.py`

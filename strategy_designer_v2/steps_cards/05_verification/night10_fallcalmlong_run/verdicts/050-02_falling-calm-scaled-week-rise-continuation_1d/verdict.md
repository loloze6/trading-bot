---
plan: 050-02_falling-calm-scaled-week-rise-continuation_1d
idea: 050-02_falling-calm-scaled-week-rise-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of the cases, taken long: 0.00643057; t of the mean, cases of one day taken together: 1.88746 (threshold: t >= 2 confirms (with positive size difference), t <= -2 rejects, otherwise inconclusive)
- Supporting check: mean unusual move of cases with forecast >= median minus those below (Welch t) [Welch t = -0.375]: -0.00221792, passed: False
- Counts: cases: 503, distinct days: 341
- Decided by: The t of the unusual move is between -2 and 2.
- Reading: The falling calm profile is the recorded regime 'unknown'; a case is the first bar in each 3-bar grid cell (from each window's first row) where the forecast rose by at least 2 points from its lowest level since its last bet (from 0 after a flat), the drift is the mean 3-bar return on that grid over all the coin's windows, and the day-clustered standard error uses the per-day summed deviations with a D/(D-1) correction.
- Size: unusual move +0.64 % (t 1.89, the cases of one day together: 341 days) per case over 3 bars, 0.077 of the coin's usual move (8.43 %); normal drift in its direction +0.34 %, total +0.99 %; 503 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.887 (not below 1), 503 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-02_falling-calm-scaled-week-rise-continuation_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02_falling-calm-scaled-week-rise-continuation_1d`
Measure: `measure.py`

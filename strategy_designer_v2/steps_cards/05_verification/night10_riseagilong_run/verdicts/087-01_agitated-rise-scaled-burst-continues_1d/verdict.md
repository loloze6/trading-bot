---
plan: 087-01_agitated-rise-scaled-burst-continues_1d
idea: 087-01_agitated-rise-scaled-burst-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar forward return (vs coin's mean 3-bar return) on forecast>0 grid bars: 0.0177545; t pooling the cases of one day: 1.35699 (threshold: confirm: mean > 0 with day-pooled t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: least-squares slope of excess 3-bar return on forecast: -0.00250544, passed: False
- Counts: independent case-days: 115, cases: 161
- Decided by: the t is between -2 and 2 (or undefined), meeting neither confirm nor reject (inconclusive rule).
- Reading: cases are grid bars (positions 0,3,6,... of each window) with forecast > 0 and a full 3-bar forward return inside the window; the coin's mean 3-bar return is over the same grids of all its windows; the t is the mean over a day-clustered standard error (deviations summed per UTC day, D/(D-1) correction); the plan's 30 case-days minimum, when unmet, is reported as not observable.
- Size: unusual move +0.44 % (t 0.49, the cases of one day together: 206 days) per case over 3 bars, 0.034 of the coin's usual move (8.55 %); normal drift in its direction +0.39 %, total +0.83 %; 250 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.357 (not below 1), 115 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_riseagilong_run/plans/087-01_agitated-rise-scaled-burst-continues_1d.md`
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/087-01_agitated-rise-scaled-burst-continues_1d`
Measure: `measure.py`

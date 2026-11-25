---
plan: 034-03.b1_choppy-far-below-high-falls_1d
idea: 034-03.b1_choppy-far-below-high-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 5-bar forward return on forecast (forecast < 0, 5-bar grid): 7.68519e-05; slope t (day-clustered): 0.113319 (threshold: confirm: slope > 0 with t >= 2 and deepest third mean < 0; reject: slope < 0 with t <= -2)
- Supporting check: mean drift-adjusted 5-bar return of the deepest third by |forecast|: -0.00946724, passed: True
- Counts: grid cases: 1446, distinct days: 415
- Decided by: The slope's |t| is below 2, which the plan calls inconclusive.
- Reading: Choppy profile read as the bars whose recorded regime is 'unknown' (the config's only regime with a strategy, i.e. |60-bar price evolution| <= 10), below-high as a negative raw depth value; the coin's mean 5-bar return is over all grid cells of all its windows; the t is the slope over a day-clustered standard error (per-day sums of x-deviation times residual); thirds split by sorted |forecast| with np.array_split, the deepest third being the last part.
- Size: unusual move +0.63 % (t 1.80, the cases of one day together: 1065 days) per case over 5 bars, 0.057 of the coin's usual move (12.35 %); normal drift in its direction -0.80 %, total -0.18 %; 2006 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-03.b1_choppy-far-below-high-falls_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/034-03.b1_choppy-far-below-high-falls_1d`
Measure: `measure.py`

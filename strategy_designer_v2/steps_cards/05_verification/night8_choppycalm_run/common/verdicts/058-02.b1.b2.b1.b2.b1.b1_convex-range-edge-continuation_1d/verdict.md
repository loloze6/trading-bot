---
plan: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d
idea: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward return minus coin mean 10-bar return on forecast (non-overlapping grid, non-zero forecast, pooled): 0.00164577; t of slope (day-clustered): 2.47751 (threshold: confirm: slope > 0 with t >= 2 and supporting check passed; reject: slope < 0 with t <= -2)
- Supporting check: mean directional excess return, top third of |forecast| minus bottom third: 0.0164326, passed: True
- Counts: non-overlapping grid cases with a non-zero forecast: 692, days: 188
- Decided by: The slope is positive with t >= 2 and the top third of |forecast| earns more in its direction than the bottom third.
- Reading: The situation is the regime column equal to the profile regime 'unknown' (rising calm, not vetoed) with the forecast's sign equal to the sign of the raw range position; the slope is an OLS fit with intercept and a day-clustered standard error (G/(G-1) correction); the coin's mean 10-bar return is taken on the non-overlapping grid of all its windows; thirds of |forecast| are equal-count splits of the cases sorted by |forecast|; the plan's minimum of 100 cases, if not reached, gives 'not observable'.
- Size: unusual move +1.65 % (t 2.60, the cases of one day together: 604 days) per case over 10 bars, 0.108 of the coin's usual move (16.68 %); normal drift in its direction +0.55 %, total +2.19 %; 1061 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/common/backtests/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d`
Measure: `measure.py`

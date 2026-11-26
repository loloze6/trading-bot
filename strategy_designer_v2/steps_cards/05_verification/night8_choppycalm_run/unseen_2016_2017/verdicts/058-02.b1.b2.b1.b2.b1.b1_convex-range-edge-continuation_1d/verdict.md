---
plan: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d
idea: 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward return minus coin mean 10-bar return on forecast (non-overlapping grid, non-zero forecast, pooled): -0.00164929; t of slope (day-clustered): -0.515375 (threshold: confirm: slope > 0 with t >= 2 and supporting check passed; reject: slope < 0 with t <= -2)
- Supporting check: mean directional excess return, top third of |forecast| minus bottom third: -0.126719, passed: False
- Counts: non-overlapping grid cases with a non-zero forecast: 36, days: 30
- Decided by: Only 36 non-overlapping grid cases with a non-zero forecast, below the plan's minimum of 100.
- Reading: The situation is the regime column equal to the profile regime 'unknown' (rising calm, not vetoed) with the forecast's sign equal to the sign of the raw range position; the slope is an OLS fit with intercept and a day-clustered standard error (G/(G-1) correction); the coin's mean 10-bar return is taken on the non-overlapping grid of all its windows; thirds of |forecast| are equal-count splits of the cases sorted by |forecast|; the plan's minimum of 100 cases, if not reached, gives 'not observable'.
- Size: unusual move +0.19 % (t 0.07, the cases of one day together: 45 days) per case over 10 bars, 0.055 of the coin's usual move (24.91 %); normal drift in its direction +6.84 %, total +7.02 %; 49 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d`
Measure: `measure.py`

---
plan: 058-02.b1.b2.b1_choppy-range-position-more-coins_1d
idea: 058-02.b1.b2.b1_choppy-range-position-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 5-bar forward return on forecast: 0.000391327; slope t, SE clustered by day: 0.789797 (threshold: slope t >= 2 (with top-minus-bottom third > 0) confirms; t <= -2 rejects)
- Supporting check: mean excess 5-bar return, top third minus bottom third of forecasts: 0.00891784, passed: True
- Counts: grid cases inside the profile: 1640, distinct days: 429
- Decided by: Slope t is between -2 and 2 (inconclusive rule).
- Reading: The choppy profile is read as regime 'unknown' (the only regime with a strategy); the coin's mean 5-bar return is taken over all its grid cells in all windows; OLS with intercept, cluster-robust (by UTC day) SEs with the usual G/(G-1)(N-1)/(N-K) correction; thirds are cut at the pooled 1/3 and 2/3 forecast quantiles; the plan's 'fewer than 100 cases or 60 days' is reported as not observable.
- Size: unusual move +0.40 % (t 1.20, the cases of one day together: 1194 days) per case over 5 bars, 0.019 of the coin's usual move (12.35 %); normal drift in its direction -0.03 %, total +0.37 %; 2392 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1_choppy-range-position-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1_choppy-range-position-more-coins_1d`
Measure: `measure.py`

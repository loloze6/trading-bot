---
plan: 058-02_agitated-rise-swing-scaled-giveback_1d
idea: 058-02_agitated-rise-swing-scaled-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-removed 5-bar forward return on the forecast (grid, forecast < 0): -0.000988632; slope t, day-clustered: -0.791487 (threshold: slope t >= 2 confirms (with strength > 0 and >= 50 cases); t <= -2 rejects (>= 50 cases))
- Supporting check: strength: mean drift-removed 5-bar return in the short direction over the coin's usual 5-bar move: -0.10212, passed: False
- Counts: grid cases with forecast below 0: 436, days: 224, active bars: 2229
- Decided by: The slope's t is between -2 and 2.
- Reading: Same-day cases are taken together through day-clustered standard errors of the OLS slope (with G/(G-1) correction); drift and usual move are each coin's mean and standard deviation of 5-bar returns on the non-overlapping grid of all its windows; the profile is read from the regime column ('unknown' = rising agitated), since its components are not recorded.
- Size: unusual move -0.80 % (t -1.05, the cases of one day together: 323 days) per case over 5 bars, -0.065 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total -1.44 %; 446 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-02_agitated-rise-swing-scaled-giveback_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-02_agitated-rise-swing-scaled-giveback_1d`
Measure: `measure.py`

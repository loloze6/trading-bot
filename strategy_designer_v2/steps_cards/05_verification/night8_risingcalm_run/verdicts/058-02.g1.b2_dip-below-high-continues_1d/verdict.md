---
plan: 058-02.g1.b2_dip-below-high-continues_1d
idea: 058-02.g1.b2_dip-below-high-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 5-bar excess return on forecast: 0.000443264; day-clustered OLS slope t: 1.0833 (threshold: confirm: slope > 0 with t >= 2 (and check passes); reject: slope < 0 with t <= -2; at least 300 independent cases)
- Supporting check: mean excess 5-bar return of the 20% most negative-forecast cases below 0: -0.00794765, passed: True
- Counts: independent cases: 3419, days: 617
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: Cases are all bars of each window's non-overlapping 5-bar grid (positions 0, 5, 10, ...) with a forward return, including forecast-0 bars; the 300 minimum is counted on these cases; the slope's t uses day-clustered (CR1) standard errors in an OLS with intercept; the deepest fifth is the ceil(20%) cases with the lowest forecast.
- Size: unusual move -0.18 % (t -0.52, the cases of one day together: 1163 days) per case over 5 bars, -0.015 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.76 %; 2963 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/058-02.g1.b2_dip-below-high-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02.g1.b2_dip-below-high-continues_1d`
Measure: `measure.py`

---
plan: 058-02.b1_calm-range-bottom-keeps-falling_1d
idea: 058-02.b1_calm-range-bottom-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 5-bar forward return on forecast (grid bars, forecast < 0): -0.000588368; OLS slope t, day-clustered: -0.676139 (threshold: confirm if slope t >= 2 and supporting check passes; reject if slope t <= -2)
- Supporting check: mean drift-adjusted 5-bar forward return < 0: -0.00961159, passed: True
- Counts: grid cases with forecast < 0: 281, distinct days: 162
- Decided by: slope t between -2 and 2
- Reading: Same-day clustering is a day-clustered (cluster-robust, G/(G-1) corrected) OLS standard error of the slope; the coin's mean 5-bar return is taken over the non-overlapping 5-bar grid of all its windows; the supporting check is the plain mean of the drift-adjusted returns of the same grid cases.
- Size: unusual move +1.20 % (t 2.78, the cases of one day together: 322 days) per case over 5 bars, 0.132 of the coin's usual move (10.60 %); normal drift in its direction -0.62 %, total +0.58 %; 421 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1_calm-range-bottom-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1_calm-range-bottom-keeps-falling_1d`
Measure: `measure.py`

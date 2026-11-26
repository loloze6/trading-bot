---
plan: 058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation_1d
idea: 058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-day forward return minus coin mean on forecast (grid, non-zero forecast): 0.000394405; slope t, day-clustered: 0.874575 (threshold: confirm: slope > 0 with t >= 2 on >= 100 cases and timing gain > 0; reject: slope < 0 with t <= -2 on >= 100 cases)
- Supporting check: book timing gain (mean daily return before costs minus market-rise gain): 0.000151772, passed: True
- Counts: grid cases: 1050, days of cases: 322
- Decided by: The slope's t lies between -2 and 2.
- Reading: Situation bars are bars whose regime is 'unknown' (the choppy calm profile, no veto fired) where the forecast's sign equals the sign of the raw range position; the slope's t uses OLS with an intercept and day-clustered (CR1) standard errors; the coin's mean 5-day return is taken on all grid bars of all its windows; the plan's 'fewer than 100 grid cases' is applied as the minimum count (not observable); the book's daily return is the mean over coins with a bar that day of position x next close-to-close return.
- Size: unusual move +0.71 % (t 2.12, the cases of one day together: 827 days) per case over 5 bars, 0.064 of the coin's usual move (11.68 %); normal drift in its direction +0.03 %, total +0.74 %; 1536 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation_1d`
Measure: `measure.py`

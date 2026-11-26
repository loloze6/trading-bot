---
plan: 074-01_agitated-stretch-below-rebounds_1d
idea: 074-01_agitated-stretch-below-rebounds
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar unusual forward return on forecast, grid bars with forecast > 0: 0.00235196; t of slope, same-day cases pooled (clustered by day): 1.03197 (threshold: confirm if t >= 2 (with mean unusual move > 0); reject if t <= -2; else inconclusive)
- Supporting check: mean unusual 10-bar move over the same grid bars above 0: 0.0044663, passed: True
- Counts: non-overlapping grid cases with a forecast above 0: 405, days the cases fall on: 152
- Decided by: The slope has t between -2 and 2 (inconclusive rule).
- Reading: Agitated profile read as a regime other than 'chop' (the config's veto of volatility percentile <= 0.5), below the average as raw distance < 0; slope from an OLS of each grid case's unusual 10-bar return on its forecast pooled over coins and windows, with a t from standard errors clustered by calendar day; drift is each coin's mean non-overlapping 10-bar return over all its windows; the plan's minimum of 30 cases is applied as 'not observable' per the workflow's rule.
- Size: unusual move +0.05 % (t 0.06, the cases of one day together: 329 days) per case over 10 bars, 0.017 of the coin's usual move (14.49 %); normal drift in its direction +1.30 %, total +1.36 %; 556 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/074-01_agitated-stretch-below-rebounds_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-01_agitated-stretch-below-rebounds_1d`
Measure: `measure.py`

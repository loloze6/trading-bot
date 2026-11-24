---
plan: 036-01_agitated-scaled-fall-three-day-rebound_1d
idea: 036-01_agitated-scaled-fall-three-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of 3-bar excess return on forecast, cases of a day clustered: 0.000464641; day-clustered OLS slope t: 0.718234 (threshold: confirm: t >= 2 with >= 100 cases and supporting check passing; reject: t <= -2 with >= 100 cases)
- Supporting check: forecast-weighted mean excess return close[t+1] to close[t+3]: 0.000443895, passed: True
- Counts: cases: 1192, days: 479
- Decided by: Slope t lies between -2 and 2.
- Reading: Agitated profile read from the recorded regime (not 'chop'); the regression has an intercept and a day-clustered (CR1) standard error; the supporting check's excess removes the coin's mean close[t+1]-to-close[t+3] return on the same 3-bar grid over all its windows; fewer than 100 cases is reported as 'not observable' per the minimum-count rule.
- Size: unusual move +0.37 % (t 1.11, the cases of one day together: 917 days) per case over 3 bars, 0.051 of the coin's usual move (7.96 %); normal drift in its direction +0.39 %, total +0.76 %; 1984 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/036-01_agitated-scaled-fall-three-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/036-01_agitated-scaled-fall-three-day-rebound_1d`
Measure: `measure.py`

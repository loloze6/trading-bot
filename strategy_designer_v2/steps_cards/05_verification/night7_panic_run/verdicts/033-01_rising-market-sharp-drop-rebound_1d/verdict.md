---
plan: 033-01_rising-market-sharp-drop-rebound_1d
idea: 033-01_rising-market-sharp-drop-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 3-day forward return minus coin's normal 3-day drift on forecast, in-profile grid bars: 0.000386453; OLS slope t: 1.11237 (threshold: confirm: slope t >= 2 with supporting difference > 0; reject: slope t <= -2; else inconclusive)
- Supporting check: mean 3-day forward return after forecast > 0 minus after in-profile forecast = 0: 0.00422963, passed: True
- Counts: grid bars with forecast > 0: 983, in-profile grid bars: 2224, in-profile grid bars with forecast = 0: 1241
- Decided by: Inconclusive rule: slope t between -2 and 2.
- Reading: Rising market read as regime 'unknown' (the detector's recorded decision, its component not being recorded) and a down day as a negative raw scaled_fall value; one pooled regression over all coins and windows with OLS t; the normal drift is each coin's mean 3-bar return over the non-overlapping grid of all its windows (all bars); the supporting difference uses raw forward returns on in-profile grid bars; grid bars without a 3-bar forward return in their window are left out.
- Size: unusual move +0.24 % (t 0.65, the cases of one day together: 799 days) per case over 3 bars, 0.035 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.60 %; 1681 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/033-01_rising-market-sharp-drop-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/033-01_rising-market-sharp-drop-rebound_1d`
Measure: `measure.py`

---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of (forecast/10) x (24-bar forward return minus coin's normal 24-bar drift), grid cases with forecast > 0: 0.00221597; ordinary t of the mean: 3.11443 (threshold: confirm if t >= 2 (with upper-minus-lower half difference > 0); reject if t <= -2; else inconclusive)
- Supporting check: mean excess 24-bar forward return, upper half minus lower half at median forecast: 0.00289808, passed: True
- Counts: grid cases with forecast > 0: 8432, upper half cases: 4216, lower half cases: 4216
- Decided by: The main measure's t is 2 or more and the upper-half minus lower-half difference is positive.
- Reading: Cases are bars at positions 0, 24, 48, ... of each window with forecast > 0 and a forward return inside the window; the coin's normal drift is the mean 24-bar return over all grid bars of all its windows; the upper half is forecast > median and the lower half forecast <= median; the plan's 200-case minimum, when not reached, gives 'not observable' as the workflow requires.
- Size: unusual move +0.12 % per case over 24 bars, 0.025 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.27 %; 13841 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_one-day-fall-next-day-rebound_1h`
Measure: `measure.py`

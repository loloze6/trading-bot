---
plan: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-day return minus drift after bounces, up-regime minus down-regime: 0.0216678; Welch t: 1.08333 (threshold: Welch t >= 2 with widening gap confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: larger-bounce gap minus smaller-bounce gap: 0.0301416, passed: True
- Counts: up-regime cases: 382, down-regime cases: 362, up larger: 191, up smaller: 191, down larger: 181, down smaller: 181
- Decided by: Welch t lies between -2 and 2.
- Reading: A case is the first bet (forecast rise >= 2 points on its side from its lowest level since the last bet) in each 20-bar grid cell of each window, grouped by the forecast's sign (long = 90-day up, short = down), with raw 20-day return minus the coin's mean non-overlapping 20-day return; the median split puts |forecast| above the group median in 'larger' and at or below it in 'smaller'; fewer than 30 cases in a group is reported as not observable.
- Size: unusual move +1.09 % per case over 20 bars, 0.048 of the coin's usual move (21.24 %); normal drift in its direction -0.02 %, total +1.07 %; 744 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d`
Measure: `measure.py`

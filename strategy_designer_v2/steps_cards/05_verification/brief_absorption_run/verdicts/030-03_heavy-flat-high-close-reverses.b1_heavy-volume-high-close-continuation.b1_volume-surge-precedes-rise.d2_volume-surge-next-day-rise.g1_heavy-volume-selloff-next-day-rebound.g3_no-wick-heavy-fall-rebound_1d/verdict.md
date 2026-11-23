---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x (next-day return - coin mean daily return) on forecast > 0 bars: 0.089308; t of the mean: 5.40208 (threshold: t >= 2 (with supporting check > 0) confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean excess next-day return above minus below median forecast: None, passed: None
- Counts: cases with forecast > 0: 3272, cases above median forecast: 0, cases below median forecast: 1629
- Decided by: The main measure's t is >= 2 but the supporting check fails (inconclusive rule).
- Reading: Bars without 20 prior bars inside their window (vr not recomputable from prices) are left out of the agreement share; the coin's mean daily return is the mean of all its 1-bar returns inside its windows; cases equal to the median forecast belong to neither half; the plan's 'fewer than 200 cases' minimum is reported as not observable, as the workflow requires.
- Size: unusual move +0.30 % per case over 1 bars, 0.060 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.42 %; 2658 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound_1d`
Measure: `measure.py`

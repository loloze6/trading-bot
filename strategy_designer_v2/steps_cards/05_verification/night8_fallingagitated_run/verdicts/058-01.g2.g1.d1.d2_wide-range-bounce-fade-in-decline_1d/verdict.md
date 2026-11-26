---
plan: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d
idea: 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move per case in the short direction, 1 bar: 0.00743061; t of the mean, cases pooled by day: 1.93408 (threshold: t >= 2 with supporting check passing confirms; t <= -2 rejects; at least 30 case-days)
- Supporting check: mean unusual move above-median |forecast| minus below-median: 0.013588, passed: True
- Counts: case-days: 279, cases: 486
- Decided by: The main t is between -2 and 2.
- Reading: Situation recomputed from closes inside each window (1-bar and 3-bar close returns), active bars whose 3-bar return cannot be computed in the window are left out of the agreement share; the coin's mean daily return is over all its windows' 1-bar returns; the day-pooled t uses per-day sums of case deviations from the mean with a G/(G-1) small-sample factor; the supporting check compares cases strictly above and strictly below the median |forecast|, ties at the median left out.
- Size: unusual move +1.18 % (t 2.50, the cases of one day together: 207 days) per case over 1 bars, 0.248 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +1.05 %; 339 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d`
Measure: `measure.py`

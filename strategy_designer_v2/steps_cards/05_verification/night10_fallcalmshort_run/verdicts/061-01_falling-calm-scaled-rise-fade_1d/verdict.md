---
plan: 061-01_falling-calm-scaled-rise-fade_1d
idea: 061-01_falling-calm-scaled-rise-fade
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move of short bets (drift removed, short direction): -0.00194073; t of the mean, cases' deviations summed per day: -0.282845 (threshold: confirm: mean > 0 with t >= 2 over >= 30 case-days and supporting check passing; reject: mean < 0 with t <= -2 over >= 30 case-days)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half: 0.0131371, passed: True
- Counts: case-days: 44, cases: 61
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive. No effect (common/verdicts.md): t in the idea's direction -0.283 (below 1), 44 cases (30 needed).
- Reading: Cases are short bets (a rise of the short forecast of at least 2 points from its low since the last bet) on every bar, the mean is over cases and its t sums the cases' deviations per UTC day, the drift is the coin's mean 1-day return over all its windows, and the supporting split puts |forecast| above the median in the larger half and at or below it in the smaller half.
- Size: unusual move -0.19 % (t -0.29, the cases of one day together: 44 days) per case over 1 bars, -0.039 of the coin's usual move (4.55 %); normal drift in its direction -0.09 %, total -0.29 %; 61 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.283 (below 1), 44 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/061-01_falling-calm-scaled-rise-fade_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/061-01_falling-calm-scaled-rise-fade_1d`
Measure: `measure.py`

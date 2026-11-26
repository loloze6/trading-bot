---
plan: 058-01.g2.g1_agitated-decline-upper-wick-fade_1d
idea: 058-01.g2.g1_agitated-decline-upper-wick-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move over the next bar, short direction: 0.00796291; t of the mean, clustered by day: 2.78121 (threshold: confirm t >= 2 with supporting check > 0; reject t <= -2; at least 100 distinct case days)
- Supporting check: mean unusual move, top half |forecast| minus bottom half: 0.00347347, passed: True
- Counts: distinct case days: 412, cases: 726
- Decided by: The main measure has t >= 2 and the supporting check is positive.
- Reading: Cases are the short bets of the workflow's case definition (a rise of the short forecast of at least 2 points, every bar on the 1-bar grid); the profile part of the situation is read from the recorded regime 'trending' since its 365-bar components are not recorded, the up day from closes; the supporting check splits cases at the median |forecast| (top: above, bottom: at or below); the day-clustered t uses a G/(G-1) correction; fewer than 100 case days gives 'not observable'.
- Size: unusual move +0.80 % (t 2.78, the cases of one day together: 412 days) per case over 1 bars, 0.175 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.67 %; 726 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00574 on the check folds against +0.007963 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1_agitated-decline-upper-wick-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1_agitated-decline-upper-wick-fade_1d`
Measure: `measure.py`

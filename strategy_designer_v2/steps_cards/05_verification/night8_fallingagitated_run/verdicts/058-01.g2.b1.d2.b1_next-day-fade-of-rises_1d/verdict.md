---
plan: 058-01.g2.b1.d2.b1_next-day-fade-of-rises_1d
idea: 058-01.g2.b1.d2.b1_next-day-fade-of-rises
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move of short cases (return minus coin drift, short direction): 0.00559097; t of the mean, cases of one day pooled: 2.08792 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger half of |forecast| minus smaller half: 0.00189961, passed: True
- Counts: distinct days with cases: 565, cases: 1669
- Decided by: Confirm rule met: mean unusual move above 0 with t >= 2 and the supporting check above 0.
- Reading: Cases are short-side bets (forecast deepening by >= 2 points from its least-short level since the last bet, reset at flat), the drift is the coin's mean daily return over all its windows, the t sums deviations per UTC day, the halves are the top and bottom floor(n/2) cases by |forecast| (middle case dropped if odd), the 30-day minimum gives 'not observable', and the profile is the recorded regime 'unknown'.
- Size: unusual move +0.56 % (t 2.09, the cases of one day together: 565 days) per case over 1 bars, 0.113 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.42 %; 1669 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004753 on the check folds against +0.005591 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1_next-day-fade-of-rises_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1_next-day-fade-of-rises_1d`
Measure: `measure.py`

---
plan: 058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade_1d
idea: 058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: unusual move after short bets, next day, before costs (fall positive): 0.00629713; t of the mean over case days (cases summed per day): 2.37844 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: unusual move of cases above median |forecast| minus below median (Welch t 1.282): 0.00326924, passed: True
- Counts: distinct case days: 566, cases: 1716, larger cases: 858, smaller cases: 858
- Decided by: the main mean is positive with t >= 2 and the larger-minus-smaller difference is above 0
- Reading: The plan's situation is taken as an up day (raw scaled_rise > 0, or a positive in-window close-to-close return where it is not recorded) on a bar whose regime is 'unknown' (inside the falling-agitated profile), with the depth graded so any close at or below its 20-day high qualifies; the expected side is short; cases are the holding-period bets (forecast rising in size on the short side by >= 2 points from its smallest size since the last bet, from 0 after flat or side change); the main value is the mean unusual move over cases with t over daily sums; the supporting split excludes cases exactly at the median; fewer than 30 case days is reported as 'not observable'.
- Size: unusual move +0.63 % (t 2.40, the cases of one day together: 566 days) per case over 1 bars, 0.127 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.49 %; 1716 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004799 on the check folds against +0.006297 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade_1d`
Measure: `measure.py`

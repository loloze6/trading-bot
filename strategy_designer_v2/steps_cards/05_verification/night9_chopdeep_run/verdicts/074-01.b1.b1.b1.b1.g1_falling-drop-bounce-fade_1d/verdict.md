---
plan: 074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day move on short cases (return minus coin drift, short direction): 0.0145622; t of the mean, cases pooled by day: 2.50495 (threshold: confirm: mean > 0 with day-pooled t >= 2 on >= 30 case-days and check passes; reject: mean < 0 with t <= -2 on >= 30 case-days)
- Supporting check: mean unusual move, larger-size half minus smaller-size half: None, passed: False
- Counts: case-days: 204, cases: 544, active bars: 570
- Decided by: t >= 2 but the supporting check fails (larger-size half minus smaller-size half not above 0).
- Reading: Cases are short bets per the holding-period rule (forecast magnitude rising >= 2 from its lowest level since the last bet, from 0 after flat); the t is cluster-robust with deviations summed per UTC day; the larger half is size above the median |forecast|, the smaller half at or below it; for the situation check the falling profile is 60-bar change in percent < -10 and conditions not computable from a window's prices fall back to the recorded regime.
- Size: unusual move +1.46 % (t 2.51, the cases of one day together: 204 days) per case over 1 bars, 0.290 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +1.30 %; 544 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade_1d`
Measure: `measure.py`

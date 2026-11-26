---
plan: 058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day_1d
idea: 058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual next-day move of cases (forecast falls >= 2 points): 0.00602223; t of the mean, cases pooled by day: 2.4334 (threshold: confirm: mean > 0 with day-pooled t >= 2 (and supporting diff > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of middling cases (forecast <= -5) minus that of largest rises (rise_lin post <= -18): -0.00119836, passed: False
- Counts: cases: 1577, distinct case days: 563, largest-rise days: 145, middling cases: 1251
- Decided by: Positive main measure with t >= 2 but the supporting difference is at or below 0 (or missing).
- Reading: Cases are short-side bets per the holding-period rule (forecast size rising >= 2 points from its lowest short size since the last bet, from 0 at a window's start or after a flat), on every bar since the grid is 1 bar; largest rises are up-day bars with rise_lin post_pipeline_value <= -18 whether or not they are cases, counted as distinct days; day-pooled t uses per-day summed deviations with a G/(G-1) factor.
- Size: unusual move +0.60 % (t 2.44, the cases of one day together: 563 days) per case over 1 bars, 0.122 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.47 %; 1577 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d1_middling-rises-fade-next-day_1d`
Measure: `measure.py`

---
plan: 074-01.b1_low-close-nearness-rebound_1d
idea: 074-01.b1_low-close-nearness-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move (long, drift removed), day-pooled t: 0.00841435; t of the mean, cases of one day pooled: 2.30515 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: upper-half minus lower-half mean unusual move, split at median low_close post_pipeline_value: 0.0137655, passed: True
- Counts: cases: 300, days: 169
- Decided by: Mean unusual move above 0 with t >= 2 over at least 30 cases, and the upper-half minus lower-half difference is positive.
- Reading: Situation checked as range/close over the std (ddof 1) of the last 30 in-window daily returns >= 2 and close location from the high >= 0.75 (recorded raw value, else from prices), using the location alone on the first bars of a window where 30 returns are not yet available, profile vetoes not re-checked; cases are long-side forecast rises of >= 2 points from the lowest level since the last bet, and the supporting split puts cases strictly above the median post_pipeline_value in the upper half, the rest in the lower half.
- Size: unusual move +0.84 % (t 2.31, the cases of one day together: 169 days) per case over 1 bars, 0.167 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.98 %; 300 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001001 on the check folds against +0.008414 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/074-01.b1_low-close-nearness-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01.b1_low-close-nearness-rebound_1d`
Measure: `measure.py`

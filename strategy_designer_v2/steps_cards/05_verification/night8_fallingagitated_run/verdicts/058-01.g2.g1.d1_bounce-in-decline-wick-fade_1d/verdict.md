---
plan: 058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d
idea: 058-01.g2.g1.d1_bounce-in-decline-wick-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction next-day excess return over cases (forecast < 0): 0.00779632; t of the mean, cases of one day taken together: 2.01576 (threshold: confirm: >= 100 cases, mean > 0 with t >= 2 and slope > 0; reject: >= 100 cases, mean < 0 with t <= -2)
- Supporting check: slope of short excess next-day return on |forecast| (post_pipeline_value): 0.00176484, passed: True
- Counts: cases: 475, days with cases: 274, cases in slope: 475
- Decided by: Confirm rule: at least 100 cases, mean short-direction excess return above 0 with t >= 2, and supporting slope above 0.
- Reading: The situation is checked as the regime rule rebuilt from closes inside each window (1-day return > 0 and 3-day return < 0, short side), on active bars whose 3 prior closes are in the window, without recomputing the falling-agitated profile whose 365-day volatility percentile needs history the record does not hold; the coin's mean daily return is the mean of all its 1-day returns pooled over its windows; the day-clustered t sums the cases' deviations per UTC day, with a D/(D-1) correction; the slope uses cases with a recorded post_pipeline_value.
- Size: unusual move +0.98 % (t 2.25, the cases of one day together: 202 days) per case over 1 bars, 0.218 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.86 %; 336 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.005459 on the check folds against +0.007796 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d`
Measure: `measure.py`

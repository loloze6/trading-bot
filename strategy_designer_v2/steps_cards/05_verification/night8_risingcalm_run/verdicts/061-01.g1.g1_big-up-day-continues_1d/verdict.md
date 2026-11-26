---
plan: 061-01.g1.g1_big-up-day-continues_1d
idea: 061-01.g1.g1_big-up-day-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move after a case: -0.00258307; t of the mean, same-day cases pooled: -0.838026 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; fewer than 100 cases: not decided)
- Supporting check: upper-half minus lower-half mean unusual move (median forecast split): 0.0123927, passed: True
- Counts: cases: 2954, days: 1179
- Decided by: The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: A case is the first long-side bet (forecast rise of >= 2 points from its lowest level since the last bet, reset at 0) in each 5-bar grid cell of a window, its return taken from that bar's close; the median split puts forecasts above the median in the upper half and the rest in the lower half; the day-pooled t uses the clustered standard error with a D/(D-1) correction; fewer than 100 cases is reported as not observable.
- Size: unusual move -0.26 % (t -0.84, the cases of one day together: 1179 days) per case over 5 bars, -0.027 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.33 %; 2954 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.g1_big-up-day-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.g1_big-up-day-continues_1d`
Measure: `measure.py`

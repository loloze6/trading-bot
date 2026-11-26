---
plan: 069-02.d1_falling-market-below-high-up-day-fade_1d
idea: 069-02.d1_falling-market-below-high-up-day-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean short-direction excess next-day return: 0.00457587; t of weighted mean, same-day cases summed: 2.29117 (threshold: confirm: > 0 with t >= 2 and rank correlation > 0; reject: < 0 with t <= -2)
- Supporting check: Spearman rank corr |forecast| vs short excess: 0.0483725, passed: True
- Counts: case-days: 2948, distinct days: 1126
- Decided by: Weighted mean short excess return above 0 with t >= 2 and rank correlation above 0 (confirm rule).
- Reading: The falling profile is recomputed from closes as a 60-bar price change below -10 % inside each window and active bars whose first 60 window bars do not allow it are left out of the agreement share; the plan's '100 case-days' is read as 100 (coin, day) cases with a nonzero forecast and a next-day return in the window, and the weighted t sums each day's weighted deviations into one piece.
- Size: unusual move +0.57 % (t 2.97, the cases of one day together: 750 days) per case over 1 bars, 0.122 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.45 %; 1658 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00162 on the check folds against +0.004576 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/069-02.d1_falling-market-below-high-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d1_falling-market-below-high-up-day-fade_1d`
Measure: `measure.py`

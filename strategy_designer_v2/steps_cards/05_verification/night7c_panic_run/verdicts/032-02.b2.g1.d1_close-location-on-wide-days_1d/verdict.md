---
plan: 032-02.b2.g1.d1_close-location-on-wide-days_1d
idea: 032-02.b2.g1.d1_close-location-on-wide-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of daily-summed (forecast/10) x next-day excess return: 0.0134525; t of the mean over days: 3.04721 (threshold: confirm t >= 2 with top-minus-bottom third difference > 0; reject t <= -2)
- Supporting check: top minus bottom third by |forecast| of sign(forecast) x next-day excess return: 0.00320586, passed: True
- Counts: days with cases: 2897, days in main measure: 2898, bars in main measure: 17380
- Decided by: The main measure's t is 2 or more and the top-minus-bottom third difference is above 0.
- Reading: Every recorded bar with a next-day return in its window is used (zero forecasts included in the daily sums and in the pooled tercile split by |forecast|, ties broken by order), days are UTC dates, a day with cases is one with a nonzero forecast on any coin, and the plan's 1000-day minimum is reported as 'not observable'.
- Size: unusual move +0.20 % (t 2.54, the cases of one day together: 2798 days) per case over 1 bars, 0.043 of the coin's usual move (4.78 %); normal drift in its direction -0.01 %, total +0.20 %; 11362 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003089 on the check folds against +0.01345 on every fold
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g1.d1_close-location-on-wide-days_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1.d1_close-location-on-wide-days_1d`
Measure: `measure.py`

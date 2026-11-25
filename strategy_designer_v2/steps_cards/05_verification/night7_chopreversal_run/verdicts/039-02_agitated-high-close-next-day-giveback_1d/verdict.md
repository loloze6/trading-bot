---
plan: 039-02_agitated-high-close-next-day-giveback_1d
idea: 039-02_agitated-high-close-next-day-giveback
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day return minus coin mean daily return on forecast: 0.00100711; slope t, day-clustered: 2.95764 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: bars in the profile: 7715, distinct days: 2214
- Decided by: The slope is positive with t >= 2: the higher the close, the larger the next-day fall.
- Reading: The agitated profile is read as regime 'unknown' (not 'chop'); the slope is an OLS slope with intercept on all profile bars with a non-zero forecast and a next bar in the same window, its t day-clustered (CR1); the plan's minimums (500 bars, 250 days) are applied as 'not observable'.
- Size: unusual move +0.39 % (t 2.77, the cases of one day together: 1597 days) per case over 1 bars, 0.092 of the coin's usual move (4.73 %); normal drift in its direction -0.00 %, total +0.39 %; 3587 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003521 on the check folds against +0.001007 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/039-02_agitated-high-close-next-day-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/039-02_agitated-high-close-next-day-giveback_1d`
Measure: `measure.py`

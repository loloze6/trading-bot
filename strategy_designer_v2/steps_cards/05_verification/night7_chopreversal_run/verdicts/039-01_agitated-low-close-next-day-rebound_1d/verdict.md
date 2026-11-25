---
plan: 039-01_agitated-low-close-next-day-rebound_1d
idea: 039-01_agitated-low-close-next-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day excess return on forecast: 0.00100711; day-clustered t of the slope: 2.95783 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects)
- Supporting check: book mean daily return before costs minus market-rise part (timing): 0.000146244, passed: True
- Counts: bars with a non-zero forecast: 7715, distinct days: 2214
- Decided by: The slope is positive with t >= 2 and the timing part is above 0.
- Reading: The agitated situation is every bar whose regime is not 'chop'; the expected side is long when the standardised close location (rebuilt from raw values with 60 past bars inside the window, else the recorded post-pipeline value) exceeds 10; the slope's t uses day-clustered standard errors with a G/(G-1) correction; the book's daily return before costs is the position after each bar's trade times the next-day return, averaged over the coins each day; and the minimum counts are applied as 'not observable'.
- Size: unusual move +0.39 % (t 2.77, the cases of one day together: 1597 days) per case over 1 bars, 0.092 of the coin's usual move (4.73 %); normal drift in its direction -0.00 %, total +0.39 %; 3587 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003521 on the check folds against +0.001007 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/039-01_agitated-low-close-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/039-01_agitated-low-close-next-day-rebound_1d`
Measure: `measure.py`

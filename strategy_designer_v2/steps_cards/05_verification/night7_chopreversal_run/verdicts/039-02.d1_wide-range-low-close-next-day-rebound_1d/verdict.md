---
plan: 039-02.d1_wide-range-low-close-next-day-rebound_1d
idea: 039-02.d1_wide-range-low-close-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (next-day return - coin mean daily return) x position held, on non-zero positions: 0.00108876; t of the mean (cases of one day summed): 2.61377 (threshold: confirm: t >= 2 with supporting check > 0; reject: t <= -2; otherwise inconclusive; minimum 300 position days on 150 distinct days)
- Supporting check: top third minus bottom third of non-zero forecasts, drift-adjusted next-day return: 0.00880166, passed: True
- Counts: position days: 9226, distinct days: 2571
- Decided by: The main measure's t is 2 or more and the supporting check is above 0 (confirm rule).
- Reading: Agitated profile read as regime 'unknown' (the non-chop regime carrying the strategy) and the situation as a raw value above 0 there, long; positions are postRebalance_current_allocation != 0 with a next-day return in the same window, every bar counted (1-bar horizon), the t uses per-day sums of the products across coins, the coin mean is over all its windows' daily returns, and the thirds are floor(n/3) lowest and highest non-zero forecasts pooled over all coins; fewer cases than the plan's minimums is reported as 'not observable'.
- Size: unusual move +0.25 % (t 1.38, the cases of one day together: 1264 days) per case over 1 bars, 0.054 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.38 %; 2847 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0009886 on the check folds against +0.001089 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/039-02.d1_wide-range-low-close-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/039-02.d1_wide-range-low-close-next-day-rebound_1d`
Measure: `measure.py`

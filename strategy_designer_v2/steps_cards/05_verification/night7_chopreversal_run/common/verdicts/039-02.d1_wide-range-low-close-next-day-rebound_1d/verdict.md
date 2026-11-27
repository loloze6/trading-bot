---
plan: 039-02.d1_wide-range-low-close-next-day-rebound_1d
idea: 039-02.d1_wide-range-low-close-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (next-day return - coin mean daily return) x position held, on non-zero positions: 0.000818285; t of the mean (cases of one day summed): 1.66081 (threshold: confirm: t >= 2 with supporting check > 0; reject: t <= -2; otherwise inconclusive; minimum 300 position days on 150 distinct days)
- Supporting check: top third minus bottom third of non-zero forecasts, drift-adjusted next-day return: 0.00613549, passed: True
- Counts: position days: 18993, distinct days: 3108
- Decided by: The main measure's t is between -2 and 2 (inconclusive rule).
- Reading: Agitated profile read as regime 'unknown' (the non-chop regime carrying the strategy) and the situation as a raw value above 0 there, long; positions are postRebalance_current_allocation != 0 with a next-day return in the same window, every bar counted (1-bar horizon), the t uses per-day sums of the products across coins, the coin mean is over all its windows' daily returns, and the thirds are floor(n/3) lowest and highest non-zero forecasts pooled over all coins; fewer cases than the plan's minimums is reported as 'not observable'.
- Size: unusual move +0.04 % (t 0.27, the cases of one day together: 1977 days) per case over 1 bars, 0.007 of the coin's usual move (5.12 %); normal drift in its direction +0.12 %, total +0.17 %; 7249 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/039-02.d1_wide-range-low-close-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/common/backtests/039-02.d1_wide-range-low-close-next-day-rebound_1d`
Measure: `measure.py`

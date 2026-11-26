---
plan: 039-02.d1_wide-range-low-close-next-day-rebound_1d
idea: 039-02.d1_wide-range-low-close-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (next-day return - coin mean daily return) x position held, on non-zero positions: -1.05536e-05; t of the mean (cases of one day summed): -0.00775359 (threshold: confirm: t >= 2 with supporting check > 0; reject: t <= -2; otherwise inconclusive; minimum 300 position days on 150 distinct days)
- Supporting check: top third minus bottom third of non-zero forecasts, drift-adjusted next-day return: -0.00414032, passed: False
- Counts: position days: 983, distinct days: 307
- Decided by: The main measure's t is between -2 and 2 (inconclusive rule).
- Reading: Agitated profile read as regime 'unknown' (the non-chop regime carrying the strategy) and the situation as a raw value above 0 there, long; positions are postRebalance_current_allocation != 0 with a next-day return in the same window, every bar counted (1-bar horizon), the t uses per-day sums of the products across coins, the coin mean is over all its windows' daily returns, and the thirds are floor(n/3) lowest and highest non-zero forecasts pooled over all coins; fewer cases than the plan's minimums is reported as 'not observable'.
- Size: unusual move -0.38 % (t -1.07, the cases of one day together: 150 days) per case over 1 bars, -0.067 of the coin's usual move (3.33 %); normal drift in its direction +0.05 %, total -0.33 %; 297 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/039-02.d1_wide-range-low-close-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2026/backtests/039-02.d1_wide-range-low-close-next-day-rebound_1d`
Measure: `measure.py`

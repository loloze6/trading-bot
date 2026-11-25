---
plan: 032-02.b2.g2.d2_below-midrange-close-rebound_1d
idea: 032-02.b2.g2.d2_below-midrange-close-rebound
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day return minus coin's mean daily return (bars with forecast > 0): 0.00385884; t of the forecast-weighted mean, cases of one day summed: 1.96777 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; else inconclusive; fewer than 100 distinct days -> not observable)
- Supporting check: none
- Counts: distinct days with a positive forecast: 1369, bars with a positive forecast: 3522
- Decided by: the t lies between -2 and 2 (inconclusive rule).
- Reading: every bar with forecast > 0 and a next close in the same window is a case, the coin's mean is the mean of all its in-window 1-bar returns, the t is the weighted mean over a standard error built from the forecast-weighted deviations summed per UTC day, and days are counted over these usable cases.
- Size: unusual move +0.33 % (t 1.47, the cases of one day together: 857 days) per case over 1 bars, 0.078 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.45 %; 1817 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g2.d2_below-midrange-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g2.d2_below-midrange-close-rebound_1d`
Measure: `measure.py`

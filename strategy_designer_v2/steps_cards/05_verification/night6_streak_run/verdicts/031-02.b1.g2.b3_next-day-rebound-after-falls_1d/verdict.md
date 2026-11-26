---
plan: 031-02.b1.g2.b3_next-day-rebound-after-falls_1d
idea: 031-02.b1.g2.b3_next-day-rebound-after-falls
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: timing gain before costs on forecast>0 bars (position x (next-day return - coin mean)), summed per day across coins, mean over days: 0.00518168; t of the mean over days: 2.38844 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2 and top-minus-bottom < 0)
- Supporting check: mean next-day excess return, top third minus bottom third by forecast: 0.00633402, passed: True
- Counts: distinct days with forecast > 0: 2199, bars with forecast > 0: 8514, bars per third: 2838
- Decided by: Confirm rule: the daily timing gain has a mean above 0 with t >= 2 and the top third beats the bottom third.
- Reading: Days are UTC calendar dates of the bar's timestamp; the 300-day minimum counts distinct dates of forecast>0 bars with a valid next-day return inside their window; thirds are the n//3 highest and n//3 lowest forecast>0 bars pooled across coins after a stable sort by forecast; the excess return removes the coin's mean daily return over all its windows.
- Size: unusual move +0.19 % (t 1.49, the cases of one day together: 1687 days) per case over 1 bars, 0.039 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.31 %; 5619 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.g2.b3_next-day-rebound-after-falls_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2.b3_next-day-rebound-after-falls_1d`
Measure: `measure.py`

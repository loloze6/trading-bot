---
plan: N5-03_high-in-confirmed-uptrend_1d_oos2
idea: N5-03_high-in-confirmed-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 10-bar return minus coin mean, forecast >= 10: 0.0467418; t of the mean (non-overlapping samples): 0.92899 (threshold: mean excess 10-bar return > 0 with t >= 2 to confirm, < 0 with t <= -2 to reject, at least 30 non-overlapping cases with forecast >= 10)
- Supporting check: Spearman rank correlation forecast vs forward 10-bar excess return, trending bars: 0.121959, passed: True
- Counts: non-overlapping cases with forecast >= 10: 49, bars with forecast >= 10: 498, trending bars: 1323
- Decided by: With at least 30 non-overlapping cases, t lies between -2 and 2 (or sign and t disagree), meeting neither confirm nor reject.
- Reading: The situation is checked as regime == 'trending' with raw range position > 0 and a long forecast; the coin's mean is its mean forward 10-bar return over all bars of all its windows; the reported value is the mean over all bars with forecast >= 10, while the t-statistic and the case count use the non-overlapping grid (positions 0, 10, 20, ... of each window).
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N5-03_high-in-confirmed-uptrend_1d_oos2.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N5-03_high-in-confirmed-uptrend_1d_oos2`
Measure: `measure.py`

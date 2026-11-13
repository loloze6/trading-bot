---
plan: N5-03_high-in-confirmed-uptrend_1d_oos
idea: N5-03_high-in-confirmed-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 10-bar excess return after forecast >= 10: 0.0294416; t of the mean, non-overlapping samples: 0.745388 (threshold: confirm if mean > 0 with t >= 2, reject if mean < 0 with t <= -2, at least 30 non-overlapping cases)
- Supporting check: Spearman rank correlation, forecast vs forward 10-bar excess return, trending bars: 0.0709526, passed: True
- Counts: non-overlapping cases with forecast >= 10: 179, bars with forecast >= 10: 1608, trending bars: 4048
- Decided by: With at least 30 non-overlapping cases, the t-statistic lies between -2 and 2 (or does not agree with the mean's sign), which the plan calls inconclusive.
- Reading: The situation is checked as regime == 'trending' (the detector's 200-SMA and 60-bar rules) with the raw 20-bar Donchian range position above 0 (upper half of the range) and a positive forecast; the coin's usual move is the mean of all its in-window 10-bar returns over all windows; the main value is the mean excess return over all bars with forecast >= 10, its t is the ordinary t of the mean over the non-overlapping grid bars (positions 0, 10, 20, ... of each window) with forecast >= 10, which are also the counted cases.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N5-03_high-in-confirmed-uptrend_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N5-03_high-in-confirmed-uptrend_1d_oos`
Measure: `measure.py`

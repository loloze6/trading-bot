---
plan: 017-01_presettle-drop-after-uptrend_1h
idea: 017-01_presettle-drop-after-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (-forecast/10) x excess 2-bar return over settlement episodes: 9.45878e-05; ordinary t: 0.845984 (threshold: confirm if t >= 2 (with check difference < 0); reject if t <= -2)
- Supporting check: mean excess 2-bar return, top third minus bottom third by |forecast|: 0.000267341, passed: False
- Counts: episodes with forecast < 0: 26436
- Decided by: The main-measure t lies between -2 and 2.
- Reading: The situation is a pre-settlement clock bar (hour mod 8 in {5,6} or in {6,7}, the better of the two stamp conventions), a positive raw 72-bar rise and a negative forecast; cases are the bars stamped 21:00/05:00/13:00 with forecast < 0 whose t+2 close lies in the same window, the coin mean is over its non-overlapping 2-bar grid across all windows, and the thirds are the n//3 largest and n//3 smallest |forecast| cases.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-01_presettle-drop-after-uptrend_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-01_presettle-drop-after-uptrend_1h`
Measure: `measure.py`

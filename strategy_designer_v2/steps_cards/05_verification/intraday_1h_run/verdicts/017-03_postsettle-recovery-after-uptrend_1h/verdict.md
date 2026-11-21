---
plan: 017-03_postsettle-recovery-after-uptrend_1h
idea: 017-03_postsettle-recovery-after-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of excess 2-bar return on forecast at settlement entry bars: 1.96278e-05; OLS slope t: 1.38867 (threshold: confirm if slope t >= 2 with forecast-weighted mean excess > 0; reject if slope t <= -2)
- Supporting check: forecast-weighted mean excess 2-bar return: 0.000357824, passed: True
- Counts: cases pooled across coins and windows: 26465
- Decided by: The slope t is between -2 and 2.
- Reading: Situation bars are those stamped 23:00, 00:00, 07:00, 08:00, 15:00, 16:00 UTC with a positive raw 72-bar rise (recorded last_history_value, else recomputed from closes), expected side long; t+2 is two rows later in the same window; the coin's mean 2-bar return is pooled over all windows on the non-overlapping grid 0,2,4,...; the slope t is the ordinary OLS slope t of excess return on forecast, pooled over all coins and windows.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-03_postsettle-recovery-after-uptrend_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-03_postsettle-recovery-after-uptrend_1h`
Measure: `measure.py`

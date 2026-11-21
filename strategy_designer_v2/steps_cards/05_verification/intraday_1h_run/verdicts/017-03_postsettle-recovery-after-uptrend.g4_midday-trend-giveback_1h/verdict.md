---
plan: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h
idea: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 10:00-bar excess 3h return on forecast (pooled): 4.37928; OLS slope t: 4.37928 (threshold: t >= 2 confirms (with >= 500 cases and supporting check), t <= -2 rejects (with >= 500 cases))
- Supporting check: mean before-cost excess gain of position over 11:00-13:00 bars: 9.50223e-05, passed: True
- Counts: daily cases: 17334, supporting check bars: 52100
- Decided by: The slope's t is 2 or more with at least 500 cases and the supporting check passes.
- Reading: Situation bars are those stamped 10:00, 11:00, 12:00 UTC (next bar starts 11-13) with expected side minus the sign of the 72-bar return; close[t+3] is taken positionally inside the window; the coin's mean 3-bar return uses the non-overlapping grid 0,3,6,... of each window pooled over windows; the supporting check uses the positions after the 10:00, 11:00 and 12:00 bars' trades, held over the 11:00-13:00 bars, against the coin's mean hourly return over all windows.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h`
Measure: `measure.py`

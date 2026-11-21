---
plan: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h
idea: 017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean of forecast/10 x excess 2-bar return from the 16:00 slot open: 0.00126971; ordinary t of the mean: 8.07009 (threshold: confirm: mean > 0 with ordinary t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2)
- Supporting check: signed excess 2-bar return, top third minus bottom third of |forecast| (Welch t >= 1): 0.00136094, passed: True
- Counts: independent cases: 17452
- Decided by: The main mean is above 0 with t >= 2 and the supporting check passes (Welch t >= 1, top third larger).
- Reading: Cases are the rows stamped 15:00 UTC with close[t+2] taken two rows later in the same window; cases with forecast 0 are kept; the coin's mean 2-bar return is the mean over the non-overlapping grid (positions 0, 2, 4, ...) of all its windows pooled; thirds are n//3 cases by |forecast| (stable sort); the 300 minimum is checked on the number of cases.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-04_postsettle-decline-after-downtrend.g3_afternoon-continuation-of-3-day-trend_1h`
Measure: `measure.py`

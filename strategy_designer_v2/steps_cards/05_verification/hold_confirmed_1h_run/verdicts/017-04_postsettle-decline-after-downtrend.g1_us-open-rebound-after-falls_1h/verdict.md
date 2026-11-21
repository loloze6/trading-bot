---
plan: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 2-bar return from the 11:00 bar's close, pooled over coins: 0.0010792; ordinary t of the mean: 4.05505 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 300 cases)
- Supporting check: OLS slope of excess 2-bar return on forecast: 0.000140573, passed: True
- Counts: cases: 8382
- Decided by: The main measure has a mean above 0 with t >= 2 and the slope is above 0.
- Reading: The 2-bar return runs from the close of the bar stamped 11:00 to the close of the bar stamped 13:00 of the same window (cases without that bar are dropped), the coin's mean 2-bar return is taken on the non-overlapping grid 0, 2, 4, ... of each window pooled over all windows, and fewer than 300 cases is reported as not observable.
- Size: unusual move +0.07 % per case over 2 bars, 0.047 of the coin's usual move (1.47 %); normal drift in its direction +0.01 %, total +0.08 %; 8748 cases
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h`
Measure: `measure.py`

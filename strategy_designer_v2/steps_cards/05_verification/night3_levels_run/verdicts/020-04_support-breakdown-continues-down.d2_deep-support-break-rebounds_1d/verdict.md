---
plan: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d
idea: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar return of the top-fifth forecast cases: 0.00174247; t of the mean: 0.435767 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 top-fifth cases)
- Supporting check: none
- Counts: positive-forecast grid cases: 2346, top-fifth cases: 815
- Decided by: The t of the mean unusual 5-bar return of the top-fifth cases lies between -2 and 2.
- Reading: Bars with a missing raw component value count as not in the situation; the top fifth is the grid cases whose forecast is at or above the 80th percentile of all positive-forecast grid cases pooled over coins and windows (ties included); the coin's mean 5-bar return is taken over all non-overlapping 5-bar grid returns of all its windows; cases without a full 5-bar return inside their window are left out.
- Size: unusual move -0.19 % per case over 5 bars, -0.012 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.39 %; 1076 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d`
Measure: `measure.py`

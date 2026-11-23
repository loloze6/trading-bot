---
plan: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess 24-bar return on forecast (settlement bars, forecast >= 2): 3.29881; OLS slope t: 3.29881 (threshold: confirm if t >= 2 with weighted mean > 0; reject if t <= -2 with weighted mean < 0; at least 200 independent cases)
- Supporting check: forecast-weighted mean excess 24-bar return > 0: 0.00178733, passed: True
- Counts: independent cases: 11231, active bars: 16923
- Decided by: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reading: Settlement bars are those whose close (start + 1h) is 00:00 or 16:00 UTC; the situation's fall is a negative raw component value (2-bar price return when missing); grid cells are positions //24 from each window's first row, the first forecast>=2 settlement bar per cell is the case and is dropped if its 24-bar return leaves the window; drift is the mean of each coin's non-overlapping 24-bar returns over all windows; the plan's 'fewer than 200 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.09 % per case over 24 bars, 0.017 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.23 %; 11246 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h`
Measure: `measure.py`

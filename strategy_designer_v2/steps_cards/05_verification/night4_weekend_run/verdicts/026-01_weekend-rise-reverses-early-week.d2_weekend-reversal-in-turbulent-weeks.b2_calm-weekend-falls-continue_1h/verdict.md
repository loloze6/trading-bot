---
plan: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h
idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 48-bar move beyond the coin's drift: 0.00884694; t of the mean: 3.05629 (threshold: t >= 2 to confirm, t <= -2 to reject, over at least 100 cases)
- Supporting check: mean move of cases at/above median forecast size minus below median: 0.00657129, passed: True
- Counts: cases: 504, cases at or above median size: 252, cases below median size: 252
- Decided by: Confirm: t >= 2 over at least 100 cases and larger falls are followed by larger moves.
- Reading: The Monday signal bar is the bar whose close (start + 1h) is Monday 00:00 UTC; the volatility-rank condition is not rechecked because a 4380-bar rank cannot be rebuilt inside the recorded windows; a case is a Monday signal bar with forecast <= -2 (a short bet of at least the 2-point band), one per 48-bar grid cell of its window, with the coin's drift the mean of its non-overlapping 48-bar returns over all windows; the supporting check splits cases at the median absolute forecast pooled over all coins.
- Size: unusual move +0.90 % per case over 48 bars, 0.133 of the coin's usual move (6.56 %); normal drift in its direction -0.27 %, total +0.63 %; 504 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h`
Measure: `measure.py`

---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (48-bar return - drift): 0.00109182; ordinary t of the mean: 0.795946 (threshold: t >= 2 (with supporting check) confirms; t <= -2 rejects)
- Supporting check: top-quartile |forecast| directional excess minus rest: 0.000350424, passed: True
- Counts: cases: 2389, top quartile cases: 598
- Decided by: -2 < t < 2.
- Reading: The situation bars are those whose close (timestamp + 1 hour) is Sunday 00:00 UTC, with the expected side the sign of Saturday's raw scaled 24-bar move; the coin's drift is the mean of its non-overlapping 48-bar grid returns pooled over all windows; cases are all such bars with non-zero forecast and a full 48-bar forward return in the window; the top quartile is the ceil(n/4) cases with the largest |forecast| (stable sort) and the rest are all other cases.
- Size: unusual move +0.04 % per case over 48 bars, 0.013 of the coin's usual move (6.56 %); normal drift in its direction +0.05 %, total +0.08 %; 1338 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h`
Measure: `measure.py`

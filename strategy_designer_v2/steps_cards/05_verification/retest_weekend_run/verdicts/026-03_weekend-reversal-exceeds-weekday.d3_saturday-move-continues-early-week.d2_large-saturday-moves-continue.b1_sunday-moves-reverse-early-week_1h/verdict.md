---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 48-bar return on post_pipeline_value of sunday_move: 0.000381431; OLS slope t: 2.55746 (threshold: slope > 0 with t >= 2 to confirm (with check); slope < 0 with t <= -2 to reject)
- Supporting check: mean of drift-adjusted 48-bar return x sign(forecast) over |forecast| >= 2: 0.00625455, passed: True
- Counts: cases across all coins and windows: 2414, cases with |forecast| >= 2: 2018
- Decided by: The slope is positive with t >= 2 and the supporting check passes (confirm rule).
- Reading: The situation is the bar whose close (timestamp + 1h) is Monday 00:00 UTC, with the side opposite to the sign of the raw sunday_move (or Sunday's 24-bar price return where not recorded); the drift is each coin's mean of non-overlapping 48-bar returns (positions 0, 48, ... of each window) pooled over its windows; the regression is OLS with intercept of the drift-adjusted return on post_pipeline_value, and |forecast| and its sign in the supporting check are read from post_pipeline_value; cases without 48 bars ahead in their window are left out; fewer than 200 cases gives 'not observable' as the workflow requires.
- Size: unusual move +0.62 % per case over 48 bars, 0.097 of the coin's usual move (6.56 %); normal drift in its direction -0.00 %, total +0.62 %; 2021 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h`
Measure: `measure.py`

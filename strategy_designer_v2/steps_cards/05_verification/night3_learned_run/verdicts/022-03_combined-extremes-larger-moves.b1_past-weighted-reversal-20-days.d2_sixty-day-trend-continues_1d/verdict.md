---
plan: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of forecast/10 x (20-bar return minus coin's normal 20-bar drift), non-overlapping grid: 0.0125328; t of the mean: 1.12704 (threshold: confirm t >= 2 over at least 300 cases with supporting check passed; reject t <= -2 over at least 300 cases)
- Supporting check: mean unusual move in forecast's direction, larger minus smaller half of abs(forecast): -0.000361917, passed: False
- Counts: cases: 1606
- Decided by: Main-measure t lies between -2 and 2.
- Reading: All grid points (positions 0, 20, 40, ... of each window with a close 20 bars later) are cases, zero forecasts included in the main mean; the supporting split excludes zero-forecast cases (no direction) and puts abs(forecast) > median in the larger half, <= median in the smaller half; fewer than 300 cases is treated as not observable per the minimum-count rule.
- Size: unusual move +1.07 % per case over 20 bars, 0.037 of the coin's usual move (25.07 %); normal drift in its direction -0.14 %, total +0.93 %; 1380 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d`
Measure: `measure.py`

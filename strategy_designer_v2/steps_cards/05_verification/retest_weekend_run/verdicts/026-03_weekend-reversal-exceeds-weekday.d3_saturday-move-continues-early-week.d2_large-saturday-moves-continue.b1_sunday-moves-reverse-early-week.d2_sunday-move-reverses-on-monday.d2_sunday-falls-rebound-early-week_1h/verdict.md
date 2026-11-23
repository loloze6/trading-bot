---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 48h return after Sunday-close bars with forecast >= 2: 0.00249308; ordinary t of the mean: 1.06472 (threshold: t >= 2 confirms (with correlation > 0); t <= -2 rejects)
- Supporting check: correlation of forecast with 48h excess return over the cases: 0.0339522, passed: True
- Counts: cases: 990
- Decided by: The t of the mean excess 48h return is between -2 and 2 (inconclusive rule).
- Reading: The Sunday-close bar is the bar starting Sunday 23:00 UTC, the 48h return is close 48 rows later in the same window, the drift is the coin's mean over 48-row non-overlapping stretches from each window's first row, and the correlation is Pearson's.
- Size: unusual move +0.24 % per case over 48 bars, 0.044 of the coin's usual move (6.56 %); normal drift in its direction +0.27 %, total +0.51 %; 991 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week_1h`
Measure: `measure.py`

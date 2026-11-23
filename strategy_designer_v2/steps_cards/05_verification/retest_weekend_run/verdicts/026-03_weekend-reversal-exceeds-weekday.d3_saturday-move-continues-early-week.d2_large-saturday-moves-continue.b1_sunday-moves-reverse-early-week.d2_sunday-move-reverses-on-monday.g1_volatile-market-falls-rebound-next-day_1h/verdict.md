---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g1_volatile-market-falls-rebound-next-day_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g1_volatile-market-falls-rebound-next-day
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x drift-adjusted 24-bar return on the 24-bar grid, before costs: 0.00156941; t of the mean: 4.57483 (threshold: confirm if t >= 2 (with the supporting check passing); reject if t <= -2)
- Supporting check: mean drift-adjusted 24-bar return after the top fifth of positive raw values (rises): -0.00389706, passed: False
- Counts: grid bars with forecast > 0: 8432, grid bars in the main measure: 17246, grid bars in the supporting check: 1760
- Decided by: Reject rule: the main measure's t is at most -2, or the post-rise mean has a t of at most -2.
- Reading: The main mean is over all grid bars (forecast 0 bars contribute 0), the drift is the coin's mean grid 24-bar return over all windows, and the top fifth is the 80th percentile of the coin's positive raw values on the grid bars; the plan's below-200 'inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.06 % per case over 24 bars, 0.013 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.21 %; 13657 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g1_volatile-market-falls-rebound-next-day_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g1_volatile-market-falls-rebound-next-day_1h`
Measure: `measure.py`

---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: position-weighted mean 2-bar excess return from 20:00 close: 0.000777487; t of weighted mean: 7.90757 (threshold: weighted mean excess > 0 with t >= 2 (confirm, with supporting check); < 0 with t <= -2 (reject))
- Supporting check: mean excess above-median minus below-median position: -0.000183409, passed: False
- Counts: cases: 16888, cases above median position: 8444, cases below median position: 8444
- Decided by: The weighted mean excess return is above 0 with t >= 2, but the supporting check fails.
- Reading: The situation is read as the bars whose coming bar is stamped 21:00 or 22:00 UTC (bars stamped 20:00 and 21:00, so the long is held over the 21:00-23:00 stretch), long side. A case is a coin-day whose 20:00 bar has a non-zero forecast and a positive position after its trade, its return runs to the bar stamped 22:00 by timestamp, the weight is that position, the t uses the weighted mean's sandwich standard error, the supporting check compares unweighted mean excess returns of cases strictly above versus strictly below the median position, and the plan's 200-case minimum gives 'not observable' when not reached.
- Size: unusual move +0.09 % per case over 2 bars, 0.060 of the coin's usual move (1.47 %); normal drift in its direction +0.01 %, total +0.10 %; 17428 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h`
Measure: `measure.py`

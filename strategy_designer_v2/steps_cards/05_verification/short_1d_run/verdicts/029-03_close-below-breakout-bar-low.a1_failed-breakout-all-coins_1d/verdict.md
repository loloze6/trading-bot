---
plan: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d
idea: 029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed unusual 5-bar move after short bets: 0.0133029; t of the mean: 1.08607 (threshold: mean > 0 with t >= 2 over >= 30 cases (confirm); mean < 0 with t <= -2 over >= 30 cases (reject))
- Supporting check: Spearman(depth abs post_pipeline_value, short-signed unusual move) > 0: 0.199375, passed: True
- Counts: cases: 113
- Decided by: t lies between -2 and 2 (or is not computable), which the plan calls inconclusive.
- Reading: Situation bars are those where fail_depth's raw value is non-zero and a bar of the previous 3 days has a low above the close (short side = forecast < 0); a short bet is a rise of at least 2 points in -forecast from its lowest short level since the last bet (reset to 0 when the forecast is >= 0), the first bet in each 5-bar grid cell from each window's first row is the case, drift is the coin's mean non-overlapping 5-bar return over all its windows, and depth is abs(post_pipeline_value).
- Size: unusual move +1.33 % per case over 5 bars, 0.139 of the coin's usual move (12.35 %); normal drift in its direction -0.84 %, total +0.49 %; 113 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-03_close-below-breakout-bar-low.a1_failed-breakout-all-coins_1d`
Measure: `measure.py`

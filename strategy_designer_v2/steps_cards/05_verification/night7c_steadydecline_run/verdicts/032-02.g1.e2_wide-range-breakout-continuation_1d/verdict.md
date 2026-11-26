---
plan: 032-02.g1.e2_wide-range-breakout-continuation_1d
idea: 032-02.g1.e2_wide-range-breakout-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-day return on grid bars with forecast > 0: 0.00821363; ordinary t of the mean: 1.86087 (threshold: confirm: > 0 with t >= 2; reject: < 0 with t <= -2; at least 30 grid cases)
- Supporting check: slope of excess return on post_pipeline_value (t >= 1, positive): 0.00028326, passed: True
- Counts: grid cases with forecast > 0: 855, cases in slope regression: 855, active bars checked: 3204
- Decided by: The t of the mean excess 5-day return lies between -2 and 2.
- Reading: Situation recomputed from prices inside each window (28-bar close change > 0 and today's high-low range over the mean high-low range of the last 28 bars including today >= 1, long side); active bars of a window's first 28 bars, where this cannot be computed, are left out of the agreement (874 such bars); cases are grid bars (positions 0,5,10,... of each window) with forecast > 0 and a 5-bar forward return inside the window, the coin's mean taken over all its grid returns of all windows, and the slope uses post_pipeline_value of near_high. Slope t = 1.1147167976328904.
- Size: unusual move +1.02 % (t 2.33, the cases of one day together: 734 days) per case over 5 bars, 0.084 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +1.61 %; 1186 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2_wide-range-breakout-continuation_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e2_wide-range-breakout-continuation_1d`
Measure: `measure.py`

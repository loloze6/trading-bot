---
plan: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d
idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 5-day return on 90-day return (fall_depth): -9.92729e-05; slope t: -0.472992 (threshold: confirm: slope > 0 with t >= 2 (and supporting check); reject: slope < 0 with t <= -2; at least 50 cases)
- Supporting check: mean excess 5-day return in the short direction: -0.000979365, passed: False
- Counts: cases: 376
- Decided by: The slope t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Bets are the forecast.md short-side rises of at least 2 points, the first one in each 5-bar grid cell (positions 0,5,10,... of each window) on a mean_reversion bar is the case, the coin's mean 5-day return is over its non-overlapping grid samples of all windows, the slope t is the OLS slope's t of excess return on fall_depth, the plan's 'fewer than 50 cases' is treated as the minimum count (not observable), and in the situation check the bounce (1-day return over the 20-day std of daily returns, counted if any of the ddof 0/1, current-bar-in/out variants is at least 2) and the 90-day return (recorded fall_depth, else from prices) leave out of the share the active bars where they cannot be computed inside the window.
- Size: unusual move -0.10 % per case over 5 bars, -0.005 of the coin's usual move (12.24 %); normal drift in its direction -0.74 %, total -0.84 %; 376 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d`
Measure: `measure.py`

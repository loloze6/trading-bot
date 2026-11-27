---
plan: 032-02.b1_calm-fall-depth-more-coins_1d
idea: 032-02.b1_calm-fall-depth-more-coins
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered-by-day LS slope of coin excess 3-bar return on post_pipeline_value: -0.00024276; slope t, clustered by day: -0.441122 (threshold: confirm if slope t >= 2 and mean short-direction unusual move > 0; reject if slope t <= -2)
- Supporting check: mean short-direction unusual 3-bar move: -0.00379493, passed: False
- Counts: grid cases: 1016, distinct days: 425
- Decided by: The slope t lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -0.441 (below 1), 1016 cases (30 needed).
- Reading: Grid bars are positions 0,3,6,... of each window with a full 3-bar return inside the window; the coin's mean 3-bar return (the drift) is taken over all its grid bars in all windows; the slope t uses a day-clustered (UTC date) sandwich standard error with a G/(G-1) correction; the profile is read from the recorded regime and the depth from last_history_value.
- Size: unusual move -0.19 % (t -0.47, the cases of one day together: 407 days) per case over 3 bars, -0.022 of the coin's usual move (8.29 %); normal drift in its direction -0.20 %, total -0.39 %; 620 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.441 (below 1), 1016 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/032-02.b1_calm-fall-depth-more-coins_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/032-02.b1_calm-fall-depth-more-coins_1d`
Measure: `measure.py`

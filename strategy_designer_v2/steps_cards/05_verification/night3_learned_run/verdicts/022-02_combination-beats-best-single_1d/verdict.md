---
plan: 022-02_combination-beats-best-single_1d
idea: 022-02_combination-beats-best-single
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of y x (combined - best post_pipeline_value) / 10 over non-overlapping 5-bar cases: 0.000254378; ordinary t of the mean: 0.208811 (threshold: t >= 2 (with combined correlation > 0, >= 300 cases) confirms; t <= -2 rejects)
- Supporting check: Pearson correlation of y with combined post_pipeline_value > 0: -0.0317871, passed: False
- Counts: non-overlapping cases: 3254, active bars: 16676
- Decided by: The main mean's t is between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are grid bars 0,5,10,... of each window with a full 5-bar return inside the window, the drift is each coin's mean over all its grid returns, cases missing either score are left out, and fewer than 300 cases is reported as not observable per the workflow's minimum-count rule.
- Size: unusual move -0.23 % per case over 5 bars, -0.020 of the coin's usual move (10.60 %); normal drift in its direction -0.03 %, total -0.27 %; 2645 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single_1d`
Measure: `measure.py`

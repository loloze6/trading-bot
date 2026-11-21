---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 5-bar return on forecast (grid bars, before costs): 0.000637725; OLS slope t: 3.10663 (threshold: confirm: slope t >= 2 with supporting check; reject: slope t <= -2)
- Supporting check: mean excess 5-bar return on grid bars with forecast < 0 below 0: -0.00342093, passed: True
- Counts: grid bars with forecast below 0: 4943, grid bars: 7128
- Decided by: Slope t >= 2 and mean excess return on forecast<0 grid bars is below 0 (confirm rule).
- Reading: Grid bars at positions 0,5,10,... of each window with the 5-bar return inside the window; coin mean is the mean of those grid returns over all its windows; the regression is OLS with an intercept over all grid bars including forecast 0; situation taken as raw component > 0 on the short side; the 200-bar minimum yields 'not observable' per the workflow.
- Size: unusual move +0.29 % per case over 5 bars, 0.020 of the coin's usual move (12.24 %); normal drift in its direction -0.75 %, total -0.46 %; 4405 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins_1d`
Measure: `measure.py`

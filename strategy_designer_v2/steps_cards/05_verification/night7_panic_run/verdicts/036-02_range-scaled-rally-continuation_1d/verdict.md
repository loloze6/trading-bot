---
plan: 036-02_range-scaled-rally-continuation_1d
idea: 036-02_range-scaled-rally-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-7-bar excess return on forecast (forecast > 0 grid cells): 0.000710098; OLS slope t: 1.43111 (threshold: confirm: slope t >= 2 and mean excess > 0 with t >= 2; reject: slope t <= -2 or mean-excess t <= -2; at least 100 cases)
- Supporting check: mean next-7-bar excess return, same-day cases summed (t >= 2, > 0): 0.0194428, passed: False
- Counts: positive-forecast grid cells: 1278, days with cases: 338
- Decided by: Neither the confirm nor the reject rule is met (slope t between -2 and 2, or positive slope with mean-excess t under 2).
- Reading: Grid cells at positions 0,7,14,... of each window with a full 7-bar forward return; the coin's mean 7-bar return is over all its grid cells in all windows; the slope is a pooled OLS across coins on per-cell values (not day-summed), while the mean-excess t uses same-day sums; the 100-case minimum counts positive-forecast cells and, being a minimum count, gives 'not observable'.
- Size: unusual move -0.15 % (t -0.33, the cases of one day together: 875 days) per case over 7 bars, -0.012 of the coin's usual move (12.44 %); normal drift in its direction +0.91 %, total +0.76 %; 1882 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/036-02_range-scaled-rally-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/036-02_range-scaled-rally-continuation_1d`
Measure: `measure.py`

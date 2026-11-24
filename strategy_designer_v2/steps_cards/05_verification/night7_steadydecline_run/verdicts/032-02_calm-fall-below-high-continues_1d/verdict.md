---
plan: 032-02_calm-fall-below-high-continues_1d
idea: 032-02_calm-fall-below-high-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 3-bar forward return minus coin's mean 3-bar return on depth post_pipeline_value (grid bars with non-zero forecast): 0.000767266; OLS slope t, clustered by day: 1.21732 (threshold: confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2; |t| < 2 inconclusive; < 100 grid cases)
- Supporting check: mean unusual 3-bar move in the short direction (minus coin drift) > 0: 0.00223553, passed: True
- Counts: independent grid cases in a position: 1071, days: 435, active bars: 3281
- Decided by: The slope's |t| is below 2, which the plan calls inconclusive.
- Reading: Profile taken from the recorded regime ('unknown' = not vetoed to chop, the detector's components are not recorded) and depth from last_history_value; the t is an OLS slope t with standard errors clustered by UTC calendar day (small-sample factor G/(G-1)*(n-1)/(n-2)); the coin's mean 3-bar return is over its non-overlapping grid of all bars of all windows; the 100-case minimum counts grid cases with a non-zero forecast and a full 3-bar forward return.
- Size: unusual move +1.06 % (t 2.60, the cases of one day together: 421 days) per case over 3 bars, 0.124 of the coin's usual move (7.96 %); normal drift in its direction -0.39 %, total +0.67 %; 618 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/032-02_calm-fall-below-high-continues_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/032-02_calm-fall-below-high-continues_1d`
Measure: `measure.py`

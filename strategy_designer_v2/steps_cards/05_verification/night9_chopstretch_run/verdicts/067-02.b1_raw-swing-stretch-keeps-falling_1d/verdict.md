---
plan: 067-02.b1_raw-swing-stretch-keeps-falling_1d
idea: 067-02.b1_raw-swing-stretch-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 10-bar return on raw stretch: 0.00155493; slope t, day-clustered: 0.177733 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean short-direction excess 10-bar return > 0: 0.00722773, passed: True
- Counts: grid cases: 200, days: 114
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: Choppy profile = regime 'unknown' (the only regime with a strategy); cases = grid bars (0,10,20,... of each window) with forecast < 0 and a 10-bar return inside the window; coin mean = mean of all its grid 10-bar returns over all windows; slope t = OLS slope over a day-clustered standard error (scores summed per day, G/(G-1) correction); the plan's 'fewer than 60 grid cases' is treated as a minimum count, so 'not observable'.
- Size: unusual move +0.32 % (t 0.44, the cases of one day together: 324 days) per case over 10 bars, 0.030 of the coin's usual move (14.49 %); normal drift in its direction -1.15 %, total -0.82 %; 424 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-02.b1_raw-swing-stretch-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1_raw-swing-stretch-keeps-falling_1d`
Measure: `measure.py`

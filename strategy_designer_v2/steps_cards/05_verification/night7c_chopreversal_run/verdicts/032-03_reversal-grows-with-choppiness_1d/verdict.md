---
plan: 032-03_reversal-grows-with-choppiness_1d
idea: 032-03_reversal-grows-with-choppiness
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of next-7-bar excess return on forecast (post_pipeline_value): -0.000827039; slope t, day-clustered: -1.9988 (threshold: slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject)
- Supporting check: slope on minus scaled 7-day move, upper minus lower half of 1 - ER(30): -0.00557219, passed: False
- Counts: grid cases with a nonzero forecast: 2443, distinct days: 441, regression cases: 2443, regression days: 441, supporting cases: 1723
- Decided by: The main slope's t lies between -2 and 2.
- Reading: The regression uses every grid bar (positions 0, 7, 14, ... of each window with a full 7-bar forward return inside it) with a recorded post_pipeline_value, and its t uses day-clustered standard errors (G/(G-1) correction) so same-day cases count as one piece of evidence. The drift is each coin's mean grid return over all windows. The halves split at the pooled median of 1 - ER(30), median included in the lower half. 1 - ER and the 30-day std (ddof 1) are computed from closes inside the window only, so grid bars before bar 30 are left out of the supporting check.
- Size: unusual move -0.04 % (t -0.11, the cases of one day together: 1100 days) per case over 7 bars, 0.001 of the coin's usual move (12.44 %); normal drift in its direction -0.01 %, total -0.05 %; 2331 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-03_reversal-grows-with-choppiness_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-03_reversal-grows-with-choppiness_1d`
Measure: `measure.py`

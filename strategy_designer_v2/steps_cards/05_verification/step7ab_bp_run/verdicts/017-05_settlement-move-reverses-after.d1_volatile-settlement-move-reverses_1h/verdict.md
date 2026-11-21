---
plan: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h
idea: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (8-bar return minus coin mean 8-bar return) over settlement cases: 0.00169764; ordinary t of the mean: 5.03367 (threshold: t >= 2 confirms (with check), t <= -2 rejects, otherwise inconclusive; at least 500 cases)
- Supporting check: mean unusual move in forecast direction, larger minus smaller |forecast| half: 0.00162921, passed: True
- Counts: cases: 20171, active bars: 20315, larger half: 10085, smaller half: 10086
- Decided by: The main-measure t is 2 or more and the larger-half minus smaller-half difference is above 0.
- Reading: A settlement bar is one whose close (start + 1h) falls at 00, 08 or 16 UTC; 24-bar volatility is the std of 1-bar simple returns, compared with its 720-bar mean from the window's prices, falling back to the recorded regime where the window holds too few bars; the expected side is opposite to the sign of the raw pre_move value (or the 2-bar return); cases are settlement bars with non-zero forecast, one per 8-bar grid cell (first in the cell), with t+8 inside the window; the coin's mean 8-bar return pools the grid returns of all its windows; the larger half is |forecast| above the median, the smaller half at or below it.
- Size: unusual move +0.11 % per case over 8 bars, 0.038 of the coin's usual move (2.81 %); normal drift in its direction -0.00 %, total +0.11 %; 17840 cases
Plan: `steps_cards/03_test_plan/step7ab_bp_run/plans/017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h.md`
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h`
Measure: `measure.py`

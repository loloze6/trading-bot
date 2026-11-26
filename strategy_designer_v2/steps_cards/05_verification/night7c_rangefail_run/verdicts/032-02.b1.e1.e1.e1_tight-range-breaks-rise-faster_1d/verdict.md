---
plan: 032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster_1d
idea: 032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move, upper minus lower forecast half: -0.0114602; Welch t: -0.923645 (threshold: Welch t >= 2 confirms (with overall mean unusual move > 0); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean unusual move over all cases above 0: 0.0176214, passed: True
- Counts: cases in upper half: 242, cases in lower half: 242, cases in all: 485
- Decided by: the Welch t lies between -2 and 2, which the plan calls inconclusive
- Reading: the breakout situation is recomputed inside each window as close above the max of the prior 60 recorded closes, so only active bars with 60 prior bars in their window enter the agreement share, and the expected side is long; a case is the first long bet (a forecast rise of at least 2 points from its lowest long level since the last bet) in each 5-bar grid cell of a window, its 5-bar return taken from that bet's close inside the window; the halves are the cases ranked by forecast, the lower n//2 against the upper n//2 (the middle case dropped when n is odd).
- Size: unusual move +1.76 % (t 2.55, the cases of one day together: 356 days) per case over 5 bars, 0.157 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +2.36 %; 485 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster_1d`
Measure: `measure.py`

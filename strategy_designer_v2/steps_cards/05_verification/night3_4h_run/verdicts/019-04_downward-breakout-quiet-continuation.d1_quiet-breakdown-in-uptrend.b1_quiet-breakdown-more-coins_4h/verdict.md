---
plan: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 18-bar move per case, before costs: -0.0038928; t of the mean: -0.936478 (threshold: mean > 0 with t >= 2 over at least 30 cases to confirm; mean < 0 with t <= -2 over at least 30 cases to reject)
- Supporting check: mean unusual move, narrower half minus wider half (Welch difference > 0): -0.00468954, passed: False
- Counts: cases: 1107, narrower half cases: 554, wider half cases: 553
- Decided by: The t of the mean short-side unusual move lies between -2 and 2 with at least 30 cases.
- Reading: The situation is recomputed per window as close below the minimum low of the 12 prior bars and close/close 180 bars earlier minus 1 above 0, using the recorded regime only on a window's first bars where that history is not in the record; a case is the first short bet (rise of the short forecast's size by at least 2 points from its smallest size since the last bet, from 0 after flat or a side change) in each 18-bar grid cell from each window's first row, the drift is the coin's mean 18-bar return on that grid over all its windows, and the supporting check passes when the narrower-minus-wider mean difference is above 0.
- Size: unusual move -0.39 % per case over 18 bars, -0.018 of the coin's usual move (9.29 %); normal drift in its direction -0.54 %, total -0.93 %; 1107 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h`
Measure: `measure.py`

---
plan: 019-04_downward-breakout-quiet-continuation_4h
idea: 019-04_downward-breakout-quiet-continuation
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted 18-bar short gain per case: -0.00717156; t of the mean: -4.48562 (threshold: positive with t >= 2 confirms (with supporting check); negative with t <= -2 rejects)
- Supporting check: larger-forecast half minus smaller-forecast half drift-adjusted short gain: 0.00645289, passed: True
- Counts: independent cases: 2731, larger-forecast half: 1365, smaller-forecast half: 1366, active bars: 5616
- Decided by: The mean drift-adjusted short gain is negative with t <= -2.
- Reading: Situation computed per window as close below the minimum low of the 12 prior bars, active bars whose 12-bar history is not inside the window are left out of the agreement; a case is the first short bet (a rise of the short forecast of at least 2 points) in each 18-bar grid cell of a window, dropped if its 18-bar return leaves the window; drift is the coin's mean non-overlapping 18-bar return over all its windows; the median split puts cases above the median absolute forecast in the larger half and the rest in the smaller half.
- Size: unusual move +0.10 % per case over 18 bars, 0.012 of the coin's usual move (8.17 %); normal drift in its direction -0.41 %, total -0.31 %; 2731 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-04_downward-breakout-quiet-continuation_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-04_downward-breakout-quiet-continuation_4h`
Measure: `measure.py`

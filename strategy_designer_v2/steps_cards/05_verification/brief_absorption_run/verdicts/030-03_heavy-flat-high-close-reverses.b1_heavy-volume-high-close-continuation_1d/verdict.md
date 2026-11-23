---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar unusual move after long cases: -0.00226551; t of the mean: -0.565561 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; fewer than 30 cases is not observable)
- Supporting check: mean unusual move, larger-forecast half minus smaller half: 0.00593996, passed: True
- Counts: cases: 1578
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first long bet (forecast rise of at least 2 points from its lowest positive level since the last bet, from 0 after a flat) in each 10-bar grid cell counted from the window's first row, dropped if its 10-bar return leaves the window; the normal drift is each coin's mean non-overlapping 10-bar grid return over all its windows; the median split puts cases with forecast above the median in the larger half and the rest in the smaller half.
- Size: unusual move -0.23 % per case over 10 bars, -0.025 of the coin's usual move (14.49 %); normal drift in its direction +1.18 %, total +0.95 %; 1578 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation_1d`
Measure: `measure.py`

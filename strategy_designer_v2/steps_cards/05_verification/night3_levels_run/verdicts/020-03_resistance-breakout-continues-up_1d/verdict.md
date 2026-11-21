---
plan: 020-03_resistance-breakout-continues-up_1d
idea: 020-03_resistance-breakout-continues-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return over cases (case return minus coin's normal 5-bar drift): 0.00314608; ordinary t of the mean: 1.20155 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess return, top half minus bottom half of raw value (N x margin): 0.00242664, passed: True
- Counts: cases: 1817, top half cases: 908, bottom half cases: 909, active bars: 3207
- Decided by: t strictly between -2 and 2 (with at least 30 cases).
- Reading: A case is the first bet bar (long forecast rise of at least 2 points from its lowest level since the last bet, from 0 after a flat) in each 5-bar grid cell counted from each window's first row, dropped if its 5-bar return leaves the window; the median split puts raw values strictly above the median in the top half and the rest in the bottom half.
- Size: unusual move +0.31 % per case over 5 bars, 0.025 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +0.90 %; 1817 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up_1d`
Measure: `measure.py`

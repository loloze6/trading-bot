---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean 20-bar excess return of long cases over coin drift: 0.00347509; t of the mean: 0.29652 (threshold: confirm t >= 2 over >= 30 cases with upper-minus-lower > 0; reject t <= -2 over >= 30 cases)
- Supporting check: upper-half minus lower-half mean excess return (median forecast split): None, passed: None
- Counts: cases: 680, upper half cases: 0, lower half cases: 680
- Decided by: t is between -2 and 2 (or undefined) over at least 30 cases.
- Reading: Situation bars are bars with raw res_break value > 0 (a 90-day swing-high level crossed upward) on the long side; a case is the first long bet (forecast rise >= 2 from its lowest long level since the last bet, reset at 0 at each window start and after flat) in each 20-bar grid cell of a window with a full 20-bar return in that window; the median split puts forecasts strictly above the median in the upper half and the rest in the lower half.
- Size: unusual move +0.35 % per case over 20 bars, 0.004 of the coin's usual move (21.24 %); normal drift in its direction +2.50 %, total +2.84 %; 680 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d`
Measure: `measure.py`

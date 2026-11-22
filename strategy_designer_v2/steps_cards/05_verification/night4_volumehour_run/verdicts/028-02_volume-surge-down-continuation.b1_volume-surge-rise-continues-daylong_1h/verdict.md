---
plan: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 24-bar move over the cases (bets of the forecast): 0.000551886; t of the mean: 0.928377 (threshold: confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of cases above the median forecast minus that of cases at or below it: -0.00078605, passed: False
- Counts: cases: 5008, cases above median forecast: 2504, cases at or below median forecast: 2504
- Decided by: t between -2 and 2 is inconclusive.
- Reading: A case is the first bet (long forecast rise >= 2 points from its lowest level since the last bet, reset at 0) in each 24-bar grid cell of a window, with its 24-bar return needing to stay inside the window; the median split puts cases with forecast above the median in the larger half and the rest in the smaller; the plan's 'fewer than 30 cases' rule is applied as the minimum count giving 'not observable'.
- Size: unusual move +0.06 % per case over 24 bars, 0.012 of the coin's usual move (4.12 %); normal drift in its direction +0.15 %, total +0.20 %; 5008 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h`
Measure: `measure.py`

---
plan: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean |forecast|/10 x short-direction 48-bar excess return, cases forecast <= -2: 0.00572132; t of the mean: 2.27616 (threshold: t >= 2 over at least 100 cases confirms (with check); t <= -2 over at least 100 cases rejects)
- Supporting check: upper minus lower |forecast| half mean short excess return: -0.00105525, passed: False
- Counts: cases: 759, upper half cases: 379, lower half cases: 380
- Decided by: t >= 2 over at least 100 cases but the supporting check fails, which the plan calls inconclusive.
- Reading: Situation bars are those stamped Sunday 23:00 UTC (start time) whose raw component value (or, if missing, 48-bar price return) is negative; drift is each coin's mean 48-bar return on the grid 0,48,... of every window pooled; cases are bars with forecast <= -2 whose t+48 bar is in the same window, pooled over coins; the upper half is |forecast| strictly above the median of case |forecast|, the lower half the rest.
- Size: unusual move +0.68 % per case over 48 bars, 0.099 of the coin's usual move (6.56 %); normal drift in its direction -0.28 %, total +0.40 %; 754 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h`
Measure: `measure.py`

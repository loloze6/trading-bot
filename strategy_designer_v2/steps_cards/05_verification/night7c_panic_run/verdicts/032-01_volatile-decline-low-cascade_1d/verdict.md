---
plan: 032-01_volatile-decline-low-cascade_1d
idea: 032-01_volatile-decline-low-cascade
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed 5-day unusual move: -0.0204635 (threshold: mean > 0 with t >= 2 (and deeper-minus-shallower > 0) confirms; t <= -2 rejects)
- Supporting check: none
- Counts: distinct case days: 27, cases: 42
- Decided by: Fewer than 30 distinct case days across all coins and windows (27).
- Reading: situation bars are those the detector labelled 'trending' (it alone holds the 365-day range ratio, which a ~122-bar window cannot recompute) whose recorded raw depth (or price-recomputed break) is below 0 and whose 30-bar return, recomputed from prices when 30 prior bars exist in the window, is below 0, with a negative forecast
- Size: unusual move -2.05 % (t -0.77, the cases of one day together: 27 days) per case over 5 bars, -0.225 of the coin's usual move (10.60 %); normal drift in its direction -0.62 %, total -2.66 %; 42 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-01_volatile-decline-low-cascade_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-01_volatile-decline-low-cascade_1d`
Measure: `measure.py`

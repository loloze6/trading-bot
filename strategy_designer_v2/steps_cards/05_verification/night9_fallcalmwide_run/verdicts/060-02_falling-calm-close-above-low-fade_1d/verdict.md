---
plan: 060-02_falling-calm-close-above-low-fade_1d
idea: 060-02_falling-calm-close-above-low-fade
fit: exact
status: mismatch
---
Situation check: 51 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the bars with a nonzero forecast are falling-calm bars whose close sits above the low with a short forecast, as the plan's Fidelity requires.
- Reading: Situation = regime 'unknown' (falling calm, no veto) with raw range_usual + high_drop_usual > 0 and a short forecast; bars in a position are those with nonzero postRebalance_current_allocation and a next close in the same window; main t uses a day-clustered standard error (deviations summed per day), the supporting correlation is computed on per-day mean forecast and per-day mean excess return with t = r*sqrt(D-2)/sqrt(1-r^2) over D days.
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/060-02_falling-calm-close-above-low-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/060-02_falling-calm-close-above-low-fade_1d`
Measure: `measure.py`

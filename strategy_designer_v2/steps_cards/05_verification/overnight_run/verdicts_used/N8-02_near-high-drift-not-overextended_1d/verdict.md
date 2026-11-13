---
plan: N8-02_near-high-drift-not-overextended_1d
idea: N8-02_near-high-drift-not-overextended
fit: adapted
status: mismatch
---
Situation check: 39 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of bars with a non-zero forecast are long bars where the high is recent, the close is in the upper half of its range and above its 20-day average, and the bar is not vetoed: the config's forecast is active outside the plan's situation.
- Reading: Situation read as a conjunction of the raw readings: recent high (bars-since-high > 0), close in the upper half of the 20-day range (Donchian > 0) and close above the 20-day SMA (distance > 0), on a non-vetoed bar (regime != 'chop'), long side; the coin mean 10-bar return uses all bars of all its windows (overlapping), the slope is OLS of excess return on forecast over the non-overlapping grid (positions 0,10,20,... per window) pooled over coins, vetoed bars are regime == 'chop', and the plan's minimum of 30 cases is treated as a minimum count (not observable when unmet).
Plan: `steps_cards/03_test_plan/overnight_run/plans/N8-02_near-high-drift-not-overextended_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N8-02_near-high-drift-not-overextended_1d`
Measure: `measure.py`

---
plan: 023-01_flat-range-top-reverts-down_1d
idea: 023-01_flat-range-top-reverts-down
fit: exact
status: mismatch
---
Situation check: 89 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of non-zero-forecast bars are flat-range bars (30-bar net move <= 0.33 of the range) with the forecast on the side opposite to the close's distance from the range middle.
- Reading: Net move taken as |close[t] - close[t-29]| over the 30-bar high-low range of rows t-29..t (falling back to the recorded regime on bars with under 30 recorded bars), expected side short when the raw mid distance is above 0 and long below; the coin's mean 5-bar return is taken on the same non-overlapping grid over all its windows; the plan's 'fewer than 30 cases' is reported as not observable per the workflow's minimum-count rule.
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down_1d`
Measure: `measure.py`

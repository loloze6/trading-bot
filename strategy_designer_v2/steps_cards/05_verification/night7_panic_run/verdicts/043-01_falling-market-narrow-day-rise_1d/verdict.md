---
plan: 043-01_falling-market-narrow-day-rise_1d
idea: 043-01_falling-market-narrow-day-rise
fit: exact
status: mismatch
---
Situation check: 64 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the bars with a nonzero forecast are falling-profile days narrower than usual with a long forecast: the config also takes positions (e.g. shorts on wider-than-usual days) outside the plan's situation.
- Reading: The falling profile is read from the recorded regime ('unknown' = not vetoed), a narrow day as the narrow component's standardised value (post_pipeline_value, rebuilt from last_history_value where missing) plus the offset being above 0, and the expected side is long.
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/043-01_falling-market-narrow-day-rise_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/043-01_falling-market-narrow-day-rise_1d`
Measure: `measure.py`

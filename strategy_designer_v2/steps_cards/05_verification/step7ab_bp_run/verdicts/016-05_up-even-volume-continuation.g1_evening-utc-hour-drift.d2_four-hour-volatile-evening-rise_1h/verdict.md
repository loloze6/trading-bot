---
plan: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean 4-bar unusual move after the 21:00 UTC close, pooled: 0.000850368; ordinary t of the mean: 5.41117 (threshold: confirm if t >= 2 with a positive mean; reject if t <= -2)
- Supporting check: top minus bottom volatility-third mean unusual move (thirds per coin): 0.000780594, passed: True
- Counts: cases in total: 17170, cases in the top volatility third: 5721, cases in the bottom volatility third: 5726
- Decided by: the main t is 2 or more with a positive mean and the top-minus-bottom volatility-third difference is above 0
- Reading: a case is a bar closing at 21:00 UTC (start timestamp plus one bar) whose forecast rises from 0 by at least the 2-point band, its return is close[t+4]/close[t]-1 within the window; thirds are split per coin by forecast rank (stable sort, near-equal parts) and the top and bottom thirds are pooled over coins for the difference, its Welch t and the 30-per-third minimum.
- Size: unusual move +0.09 % per case over 4 bars, 0.043 of the coin's usual move (2.03 %); normal drift in its direction +0.02 %, total +0.11 %; 17180 cases
Plan: `steps_cards/03_test_plan/step7ab_bp_run/plans/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h.md`
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h`
Measure: `measure.py`

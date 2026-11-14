---
plan: N4-03_breakouts-pay-in-uptrends_1d
idea: N4-03_breakouts-pay-in-uptrends
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean signed 10-bar excess return over holding, |forecast| >= 10: 0.0491488; t of the mean: 2.27021 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2)
- Supporting check: per-regime signed excess return (trending mean 0.08430239198435946 t 2.905230821505342; mean_reversion mean -0.033509703700360015 t -1.7500909457178155): 2.90523, passed: False
- Counts: non-overlapping cases (pool): 124, trending cases: 87, mean_reversion cases: 37
- Decided by: Pooled mean signed excess return > 0 with t >= 2 on non-overlapping cases.
- Reading: Situation taken as the recorded Donchian component value > 0 (close in the upper part of its 20-day range) with side from the `regime` label (trending long, mean_reversion short) since the 200-day SMA cannot be rebuilt inside the windows; holding is the coin's mean of all overlapping 10-bar forward returns pooled over its windows; cases are the grid bars 0,10,20,... of each window with |forecast| >= 10; the supporting check passes when both regime sides have a positive mean.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N4-03_breakouts-pay-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-03_breakouts-pay-in-uptrends_1d`
Measure: `measure.py`

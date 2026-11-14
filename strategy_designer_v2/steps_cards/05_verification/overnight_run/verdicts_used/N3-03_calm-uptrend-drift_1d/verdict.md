---
plan: N3-03_calm-uptrend-drift_1d
idea: N3-03_calm-uptrend-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return on long bars (fwd 5-bar return minus coin's mean 5-bar return), pooled, before costs: 0.00440265; t of the mean on non-overlapping 5-bar blocks: 1.49345 (threshold: confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2 (t on non-overlapping 5-bar blocks); otherwise inconclusive)
- Supporting check: OLS slope of excess 5-bar return on forecast across long bars (should be > 0): 0.000446769, passed: True
- Counts: non-overlapping 5-bar long cases pooled across coins: 897, long bars: 4439
- Decided by: The result meets neither the confirm nor the reject rule (t between -2 and 2 or sign disagreeing), so it is inconclusive.
- Reading: The coin's mean 5-bar return is taken over all its bars' forward returns in all windows; the mean excess is over all long bars while the t uses only long bars on each window's 0,5,10,... grid; the supporting slope is reported but not part of the decision since the confirm/reject rules do not mention it.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N3-03_calm-uptrend-drift_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-03_calm-uptrend-drift_1d`
Measure: `measure.py`

---
plan: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h
idea: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 2-bar excess return (15:00 UTC bar) on recorded forecast, pooled: 9.10877e-05; ordinary OLS slope t: 9.13935 (threshold: slope t >= 2 confirms (with supporting mean > 0, >= 1000 cases); t <= -2 rejects)
- Supporting check: mean of sign(forecast) x excess 2-bar return: 0.000889779, passed: True
- Counts: cases: 17452
- Decided by: Slope t >= 2 and supporting mean > 0 from at least 1000 cases: the confirm rule.
- Reading: Cases are all bars stamped 15:00 UTC (including any with forecast 0) with close[t+2] taken two rows later in the same window; the coin's mean 2-bar return is pooled over all its windows on the non-overlapping grid 0,2,4,... of each window.
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h`
Measure: `measure.py`

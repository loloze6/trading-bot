---
plan: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h
idea: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (2-bar return minus coin mean 2-bar return): 0.000423841; ordinary t of the mean: 4.07692 (threshold: t >= 2 confirms (with quintile check), t <= -2 rejects, with at least 200 cases)
- Supporting check: top minus bottom forecast quintile mean excess 2-bar return: 0.0008883, passed: True
- Counts: cases: 50986
- Decided by: The main t is 2 or more with at least 200 cases and the top-minus-bottom quintile difference is above 0.
- Reading: The coin's mean 2-bar return is taken over all non-overlapping grid bars of all its windows, quintiles are cut on the forecast rank (ties by order), and the off-settlement situation is read from the recorded regime.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h`
Measure: `measure.py`

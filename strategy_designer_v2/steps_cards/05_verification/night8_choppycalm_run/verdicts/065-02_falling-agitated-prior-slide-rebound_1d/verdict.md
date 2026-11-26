---
plan: 065-02_falling-agitated-prior-slide-rebound_1d
idea: 065-02_falling-agitated-prior-slide-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of next-day excess return on forecast (forecast > 0): 0.000600422; day-clustered t: 1.77455 (threshold: confirm: slope > 0 with day-clustered t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: forecast slope with latest day's return added, day-clustered t: 1.9339, passed: False
- Counts: bars with forecast > 0: 3092, distinct days: 875
- Decided by: The main t lies between -2 and 2.
- Reading: The profile is the recorded regime 'unknown', the slide the raw component's sign; excess return uses each coin's mean next-day return over all its bars in all windows; SEs are CR1 clustered by UTC day; the supporting regression drops each window's first bar (no latest-day return); the plan's minimum of 100 bars and 50 days is applied as a minimum count.
- Size: unusual move +0.38 % (t 1.36, the cases of one day together: 529 days) per case over 1 bars, 0.081 of the coin's usual move (5.13 %); normal drift in its direction +0.13 %, total +0.51 %; 1403 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/065-02_falling-agitated-prior-slide-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/065-02_falling-agitated-prior-slide-rebound_1d`
Measure: `measure.py`

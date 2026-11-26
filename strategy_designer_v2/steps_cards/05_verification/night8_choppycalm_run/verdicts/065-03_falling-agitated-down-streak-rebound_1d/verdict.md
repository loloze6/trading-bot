---
plan: 065-03_falling-agitated-down-streak-rebound_1d
idea: 065-03_falling-agitated-down-streak-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast, bars with forecast > 0: -0.000145261; t (deviations summed per day): -0.360262 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean next-day return minus coin mean, forecast > 0: 0.00472449, passed: True
- Counts: distinct days with forecast > 0: 832, bars with forecast > 0: 2872
- Decided by: |t| < 2 (inconclusive rule).
- Reading: The profile is read from the recorded regime ('unknown' = both vetoes off, the falling agitated profile) and the streak from the raw down_streak value (> 0, price down-close if missing); the slope's t uses day-clustered errors (x-deviation times residual summed per day); the 100-day minimum counts distinct UTC days of bars with forecast > 0 and a next-day return, and below it the status is 'not observable'.
- Size: unusual move +0.49 % (t 2.15, the cases of one day together: 768 days) per case over 1 bars, 0.106 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.63 %; 2360 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/065-03_falling-agitated-down-streak-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/065-03_falling-agitated-down-streak-rebound_1d`
Measure: `measure.py`

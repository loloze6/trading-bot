---
plan: 010-02_rsi-below-midpoint-continues-down_1d
idea: 010-02_rsi-below-midpoint-continues-down
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the 7-bar forward excess return on the forecast (pooled, non-overlapping): 1.82336; OLS slope t: 1.82336 (threshold: confirm if t >= 2 with timing gain > 0; reject if t <= -2; at least 300 non-overlapping cases)
- Supporting check: book mean daily timing gain before costs > 0: 0.000924257, passed: True
- Counts: non-overlapping cases pooled: 815
- Decided by: The slope's t is between -2 and +2, which the plan calls inconclusive.
- Reading: The raw value is read as share-0.5 when any raw value is negative, else as the plain share, with the situation's midpoint at a share of 0.5. Bars with a missing raw value count as disagreeing. The coin's mean 7-bar return is taken over its non-overlapping samples in all its windows. The minimum of 300 cases applies to the coins present in the record. The timing gain is measured before costs, from the position held times the next bar's close-to-close return minus the position times the coin's mean daily return, averaged over coins each day.
- Size: unusual move +1.51 % per case over 7 bars, 0.130 of the coin's usual move (11.06 %); normal drift in its direction -0.08 %, total +1.42 %; 342 cases
Plan: `steps_cards/03_test_plan/night_run/plans/010-02_rsi-below-midpoint-continues-down_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/010-02_rsi-below-midpoint-continues-down_1d`
Measure: `measure.py`

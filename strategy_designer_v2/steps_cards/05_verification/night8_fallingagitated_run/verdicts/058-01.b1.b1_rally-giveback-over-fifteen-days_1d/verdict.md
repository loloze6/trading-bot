---
plan: 058-01.b1.b1_rally-giveback-over-fifteen-days_1d
idea: 058-01.b1.b1_rally-giveback-over-fifteen-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 15-bar return minus normal drift on forecast (grid bars, forecast < 0): 0.00240682; OLS slope t: 1.21005 (threshold: slope > 0 with t >= 2 on >= 30 cases confirms; slope < 0 with t <= -2 on >= 30 cases rejects)
- Supporting check: mean share given back, top half of |forecast| minus bottom half: 0.719468, passed: True
- Counts: cases: 177
- Decided by: the slope's t is between -2 and 2 on at least 30 cases
- Reading: cases are grid bars (0,15,30,... of each window) with forecast < 0 and a 15-bar return inside the window; drift is the coin's mean non-overlapping 15-bar return over all its windows; slope t is the OLS slope over its standard error; the share check keeps cases with a positive 3-day price rise ending at the signal bar and splits them by |forecast| rank into lower and upper n//2 (middle case dropped if odd); the plan's 'fewer than 30 cases' is applied as the minimum count, giving 'not observable'.
- Size: unusual move +3.72 % (t 2.49, the cases of one day together: 217 days) per case over 15 bars, 0.167 of the coin's usual move (19.78 %); normal drift in its direction -2.25 %, total +1.47 %; 450 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.b1.b1_rally-giveback-over-fifteen-days_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.b1.b1_rally-giveback-over-fifteen-days_1d`
Measure: `measure.py`

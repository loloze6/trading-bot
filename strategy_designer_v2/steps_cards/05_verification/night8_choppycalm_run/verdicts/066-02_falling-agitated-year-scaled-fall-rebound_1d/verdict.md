---
plan: 066-02_falling-agitated-year-scaled-fall-rebound_1d
idea: 066-02_falling-agitated-year-scaled-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, over bars with forecast > 0: 0.000638455; slope t, cases of one day pooled (clustered by day): 2.44417 (threshold: slope t >= 2 (with mean excess > 0) confirms; slope t <= -2 rejects)
- Supporting check: mean next-day excess return over bars with forecast > 0 above 0: 0.00489299, passed: True
- Counts: bars with forecast > 0: 2814, distinct days: 828
- Decided by: The slope's t is 2 or more and the mean excess return is above 0.
- Reading: The falling agitated profile is read from the recorded `regime` (bars left 'unknown' by the two chop vetoes, since the detector's components are not recorded and cannot be rebuilt inside ~120-bar windows), a fall is a negative raw scaled return, the slope's t is an OLS t with standard errors clustered by UTC day, and bars without a next close in the same window are left out.
- Size: unusual move +0.79 % (t 2.68, the cases of one day together: 540 days) per case over 1 bars, 0.166 of the coin's usual move (5.21 %); normal drift in its direction +0.14 %, total +0.93 %; 1647 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003831 on the check folds against +0.0006385 on every fold
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/066-02_falling-agitated-year-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/066-02_falling-agitated-year-scaled-fall-rebound_1d`
Measure: `measure.py`

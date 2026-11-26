---
plan: 066-02_falling-agitated-year-scaled-fall-rebound_1d
idea: 066-02_falling-agitated-year-scaled-fall-rebound
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, over bars with forecast > 0: 0.000857655; slope t, cases of one day pooled (clustered by day): 0.628958 (threshold: slope t >= 2 (with mean excess > 0) confirms; slope t <= -2 rejects)
- Supporting check: mean next-day excess return over bars with forecast > 0 above 0: 0.00147315, passed: True
- Counts: bars with forecast > 0: 19, distinct days: 19
- Decided by: Minimum count not reached: 19 bars with forecast > 0 (need 100) on 19 distinct days (need 60).
- Reading: The falling agitated profile is read from the recorded `regime` (bars left 'unknown' by the two chop vetoes, since the detector's components are not recorded and cannot be rebuilt inside ~120-bar windows), a fall is a negative raw scaled return, the slope's t is an OLS t with standard errors clustered by UTC day, and bars without a next close in the same window are left out.
- Size: unusual move +0.27 % (t 0.51, the cases of one day together: 8 days) per case over 1 bars, 0.023 of the coin's usual move (6.78 %); normal drift in its direction +1.02 %, total +1.29 %; 8 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/066-02_falling-agitated-year-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/066-02_falling-agitated-year-scaled-fall-rebound_1d`
Measure: `measure.py`

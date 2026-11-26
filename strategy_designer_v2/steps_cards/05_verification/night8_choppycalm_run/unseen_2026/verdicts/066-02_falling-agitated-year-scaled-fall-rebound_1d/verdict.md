---
plan: 066-02_falling-agitated-year-scaled-fall-rebound_1d
idea: 066-02_falling-agitated-year-scaled-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, over bars with forecast > 0: -3.80703e-05; slope t, cases of one day pooled (clustered by day): -0.045215 (threshold: slope t >= 2 (with mean excess > 0) confirms; slope t <= -2 rejects)
- Supporting check: mean next-day excess return over bars with forecast > 0 above 0: 0.00100661, passed: True
- Counts: bars with forecast > 0: 516, distinct days: 114
- Decided by: The slope's t is between -2 and 2.
- Reading: The falling agitated profile is read from the recorded `regime` (bars left 'unknown' by the two chop vetoes, since the detector's components are not recorded and cannot be rebuilt inside ~120-bar windows), a fall is a negative raw scaled return, the slope's t is an OLS t with standard errors clustered by UTC day, and bars without a next close in the same window are left out.
- Size: unusual move -0.17 % (t -0.27, the cases of one day together: 72 days) per case over 1 bars, -0.045 of the coin's usual move (3.93 %); normal drift in its direction +0.01 %, total -0.16 %; 286 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/066-02_falling-agitated-year-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2026/backtests/066-02_falling-agitated-year-scaled-fall-rebound_1d`
Measure: `measure.py`

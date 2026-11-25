---
plan: 032-03.b2.b1_deep-calm-decline-more-coins_1d
idea: 032-03.b2.b1_deep-calm-decline-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 10-bar forward return on the forecast: 0.000558812; OLS slope t, day-clustered SE: 0.383809 (threshold: confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean of -(10-bar return - drift) over the cases: 0.0161269, passed: True
- Counts: independent cases (distinct days): 216, cases (coin grid cells): 1179
- Decided by: The slope's t lies between -2 and 2.
- Reading: Cases are grid bars 0,10,20,... of each window with a full 10-bar forward return, regime mean_reversion and forecast < 0. The drift is the coin's mean grid 10-bar return over all its windows. 'Cases of the same day pooled' is read as a day-clustered (CR1) standard error of the slope. For the situation check, the volume ratio is rebuilt from in-window volumes where 118 bars exist, else taken from the recorded regime.
- Size: unusual move +1.28 % (t 1.77, the cases of one day together: 637 days) per case over 10 bars, 0.071 of the coin's usual move (16.53 %); normal drift in its direction -1.40 %, total -0.12 %; 1357 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-03.b2.b1_deep-calm-decline-more-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b2.b1_deep-calm-decline-more-coins_1d`
Measure: `measure.py`

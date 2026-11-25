---
plan: 032-03.b1_thin-volume-decline-more-coins_1d
idea: 032-03.b1_thin-volume-decline-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess return (return minus coin drift) on forecast, in-regime grid cases: 0.000590506; slope t, cases of a day taken together: 1.24531 (threshold: slope t >= 2 confirms (with supporting check and >=100 cases on >=60 days); t <= -2 rejects)
- Supporting check: mean 5-bar excess return on cases with forecast <= -2 below 0: -0.00865514, passed: True
- Counts: in-regime cases: 3307, distinct days: 498, cases with forecast <= -2: 1983
- Decided by: Slope t between -2 and 2: inconclusive by the plan's rule.
- Reading: Situation recomputed as close below its close 28 bars earlier inside each window, falling back to the recorded regime on a window's first 28 bars; expected side short; in-regime cases are grid bars with regime 'trending'; drift is the coin's mean 5-bar return over its non-overlapping grid of all windows; the slope's t uses day-clustered (cases summed per day) standard errors with a G/(G-1) correction; the supporting check uses in-regime grid cases with forecast <= -2.
- Size: unusual move +0.42 % (t 1.09, the cases of one day together: 814 days) per case over 5 bars, 0.024 of the coin's usual move (11.97 %); normal drift in its direction -0.79 %, total -0.37 %; 1444 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-03.b1_thin-volume-decline-more-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b1_thin-volume-decline-more-coins_1d`
Measure: `measure.py`

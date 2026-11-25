---
plan: 041-02_agitated-fall-rise-vs-range-giveback_1d
idea: 041-02_agitated-fall-rise-vs-range-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (bars with forecast < 0): -0.000134764; OLS slope t, clustered by day: -0.52486 (threshold: confirm: slope > 0 with day-clustered t >= 2 (and supporting check); reject: slope < 0 with t <= -2)
- Supporting check: mean next-day unusual move in the short direction > 0: 0.0055899, passed: True
- Counts: independent days with a negative forecast: 633, cases (bars with a negative forecast): 1326
- Decided by: The slope's t lies between -2 and 2.
- Reading: The profile is read from the recorded regime and an up-day from the raw value > 0; the slope's t is an OLS slope with standard error clustered by calendar day (correction G/(G-1)), the supporting check is the plain mean over all cases of -(next-day return - drift), and the plan's '30 independent days' minimum is the number of distinct days with a negative forecast, whose shortfall gives 'not observable'.
- Size: unusual move +0.68 % (t 2.75, the cases of one day together: 464 days) per case over 1 bars, 0.147 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.55 %; 924 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/041-02_agitated-fall-rise-vs-range-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/041-02_agitated-fall-rise-vs-range-giveback_1d`
Measure: `measure.py`

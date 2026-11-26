---
plan: 041-01_agitated-fall-rise-vs-swing-giveback_1d
idea: 041-01_agitated-fall-rise-vs-swing-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered-by-day t of the slope of next-bar excess return on abs(forecast), forecast < 0: 8.50512e-05; slope t, clustered by day: 0.268764 (threshold: confirm: slope <= 0 with t <= -2 (and mean excess < 0, >= 100 cases); reject: t >= +2)
- Supporting check: mean next-bar return minus coin drift on forecast < 0 bars, before costs, below 0: -0.0055899, passed: True
- Counts: cases (bars with forecast < 0): 1326, days: 633
- Decided by: The slope t lies between -2 and +2.
- Reading: The profile is read from the recorded regime (default 'unknown' = falling agitated, vetoes give 'chop') since its 365-bar detector cannot be rebuilt inside 120-bar windows, the rise from the raw scaled return > 0; the coin's drift is the mean of all its in-window 1-bar returns over all windows, every bar is a case at a 1-bar horizon, the slope's t uses day-clustered standard errors, and the plan's 'fewer than 100 cases' is treated as the minimum count (not observable).
- Size: unusual move +0.53 % (t 1.97, the cases of one day together: 443 days) per case over 1 bars, 0.116 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.40 %; 851 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/041-01_agitated-fall-rise-vs-swing-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/041-01_agitated-fall-rise-vs-swing-giveback_1d`
Measure: `measure.py`

---
plan: 040-01_agitated-fall-size-next-day-rebound_1d
idea: 040-01_agitated-fall-size-next-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (forecast > 0 bars): 0.00052954; OLS slope t: 3.75899 (threshold: confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2)
- Supporting check: book timing gain before costs (mean daily): 0.000454626, passed: True
- Counts: bars with forecast > 0: 3753
- Decided by: The slope is positive with t >= 2 and the timing gain is above 0 (confirm rule).
- Reading: Agitated profile read as regime 'unknown' (the volatility-percentile veto sends the rest to 'chop'), the day's fall as a negative recorded raw value (price return where not recorded); the timing gain is computed before costs as position after the bar's trade x next-bar return minus position x the coin's all-window mean daily return, averaged over coins per day then over days; the slope's t is the OLS t.
- Size: unusual move +0.33 % (t 1.66, the cases of one day together: 1083 days) per case over 1 bars, 0.074 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.46 %; 2553 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003694 on the check folds against +0.0005295 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/040-01_agitated-fall-size-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/040-01_agitated-fall-size-next-day-rebound_1d`
Measure: `measure.py`

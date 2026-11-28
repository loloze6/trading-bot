---
plan: 041-01.b1_rising-agitated-rise-continues_1d
idea: 041-01.b1_rising-agitated-rise-continues
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered t of the slope of next-day excess return on forecast (forecast > 0 bars, pooled): 4.3815e-06; day-clustered OLS slope t: 0.0154832 (threshold: t >= 2 with positive mean excess return confirms; t <= -2 rejects; otherwise inconclusive; min 100 bars)
- Supporting check: mean next-day excess return over forecast > 0 bars: -0.00114068, passed: False
- Counts: bars with forecast > 0: 1852, days: 1033
- Decided by: The slope's t lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.015 (below 1), 1033 cases (30 needed).
- Reading: The situation is a positive raw scaled one-day rise (recorded last_history_value, recomputed from closes inside the window where missing) with a long forecast; the slope's t uses OLS with standard errors clustered by UTC day (scores summed per day, G/(G-1) correction); the coin's mean daily return is over all its bars' next-day returns in all windows; the 100-bar minimum counts forecast > 0 bars with a next-day return.
- Size: unusual move -0.28 % (t -1.16, the cases of one day together: 720 days) per case over 1 bars, -0.055 of the coin's usual move (4.71 %); normal drift in its direction +0.14 %, total -0.14 %; 1185 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.015 (below 1), 1033 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_riseagilong_run/plans/041-01.b1_rising-agitated-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/041-01.b1_rising-agitated-rise-continues_1d`
Measure: `measure.py`

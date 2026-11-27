---
plan: 067-02.b1.b1.g1_choppy-agitated-month-weakness-falls_1d
idea: 067-02.b1.b1.g1_choppy-agitated-month-weakness-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean 7-bar directional excess return (short), short grid bars: 0.00704396; day-clustered t: 0.586934 (threshold: confirm: mean > 0 with t >= 2 over >= 30 days and supporting check passes; reject: t <= -2 over >= 30 days)
- Supporting check: mean excess of larger-|forecast| half minus smaller half: 0.0138159, passed: True
- Counts: independent days with a short grid case: 133, short grid cases: 276
- Decided by: |t| < 2 over at least 30 days: the result is inconclusive.
- Reading: Days are UTC calendar days of the grid bar; the day-clustered t sums each day's weighted deviations; the larger half is the top floor(n/2) cases by |forecast| (ties in record order) with unweighted half means; 'near zero' is read as covered by the |t| < 2 rule, with no extra threshold.
- Size: unusual move +0.98 % (t 1.44, the cases of one day together: 335 days) per case over 7 bars, 0.061 of the coin's usual move (12.84 %); normal drift in its direction -0.96 %, total +0.03 %; 457 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1.g1_choppy-agitated-month-weakness-falls_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.g1_choppy-agitated-month-weakness-falls_1d`
Measure: `measure.py`

---
plan: 058-02_quiet-volume-fall-continues_1d
idea: 058-02_quiet-volume-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of drift-removed 5-bar return x -forecast/10 on non-overlapping grid bars with forecast < 0: -0.00421575; t of the mean, cases of one day summed: -0.554834 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: drift-removed 5-bar return, |forecast| above median minus below: 0.000242554, passed: False
- Counts: grid cases: 444, distinct days: 193
- Decided by: The main measure's t lies between -2 and 2 (or its sign disagrees), the plan's inconclusive rule.
- Reading: Situation taken as regime 'unknown' (the falling-calm profile passed) with raw component < 0 and a short forecast; the per-day t is a day-clustered t of the case mean; the minimum is read as at least 30 grid cases and at least 30 distinct days; the median split excludes cases equal to the median; drift is the coin's mean grid 5-bar return over all its windows.
- Size: unusual move +0.87 % (t 1.40, the cases of one day together: 311 days) per case over 5 bars, 0.082 of the coin's usual move (10.60 %); normal drift in its direction -0.69 %, total +0.19 %; 443 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-02_quiet-volume-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-02_quiet-volume-fall-continues_1d`
Measure: `measure.py`

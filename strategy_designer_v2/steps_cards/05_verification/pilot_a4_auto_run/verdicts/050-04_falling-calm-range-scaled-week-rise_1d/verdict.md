---
plan: 050-04_falling-calm-range-scaled-week-rise_1d
idea: 050-04_falling-calm-range-scaled-week-rise
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 3-day excess return (forward return minus coin's mean 3-day return): 0.00697167; t of weighted mean, cases of one day summed: 1.26174 (threshold: confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2)
- Supporting check: mean excess above median forecast minus below median: 0.00582749, passed: True
- Counts: cases: 389, days: 204
- Decided by: The t of the main measure lies between -2 and 2.
- Reading: The falling-calm profile is read from the recorded regime ('unknown' = no veto fired) and the 7-day rise from the sign of the raw component (7-day close return where missing); all coins in the record are used; the t of the weighted mean uses per-day sums of weighted deviations (clustered standard error with G/(G-1) correction); the median split drops cases exactly at the median and compares unweighted mean excess returns.
- Size: unusual move +0.54 % (t 1.31, the cases of one day together: 302 days) per case over 3 bars, 0.058 of the coin's usual move (8.29 %); normal drift in its direction +0.20 %, total +0.75 %; 458 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.262 (not below 1), 389 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/050-04_falling-calm-range-scaled-week-rise_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/050-04_falling-calm-range-scaled-week-rise_1d`
Measure: `measure.py`

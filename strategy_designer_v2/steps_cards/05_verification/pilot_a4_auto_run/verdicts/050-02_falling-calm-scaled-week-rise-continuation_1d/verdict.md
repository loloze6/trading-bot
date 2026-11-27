---
plan: 050-02_falling-calm-scaled-week-rise-continuation_1d
idea: 050-02_falling-calm-scaled-week-rise-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move after a forecast rise of >= 2 points: 0.00619238; t of the mean, cases of the same day summed: 1.50108 (threshold: confirm: mean > 0 with day-clustered t >= 2; reject: t <= -2)
- Supporting check: upper minus lower half (forecast median split) mean unusual move: 0.00452563, passed: False
- Counts: cases: 467, upper half cases: 233, lower half cases: 234, days with cases: 303
- Decided by: Neither the confirm nor the reject rule holds (a t between -2 and 2 on the main measure or the supporting check).
- Reading: A case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, from 0 after flat) in each 3-bar grid cell counted from each window's first row, drift is the coin's mean grid 3-bar return over all its windows, the upper half is forecast > median and the lower half forecast <= median, the day-clustered t uses a D/(D-1) correction, and the plan's 'too few cases is inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.62 % (t 1.50, the cases of one day together: 303 days) per case over 3 bars, 0.067 of the coin's usual move (8.29 %); normal drift in its direction +0.21 %, total +0.82 %; 467 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.501 (not below 1), 233 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/050-02_falling-calm-scaled-week-rise-continuation_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/050-02_falling-calm-scaled-week-rise-continuation_1d`
Measure: `measure.py`

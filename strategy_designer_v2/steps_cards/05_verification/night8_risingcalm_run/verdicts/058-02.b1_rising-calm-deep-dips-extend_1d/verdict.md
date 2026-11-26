---
plan: 058-02.b1_rising-calm-deep-dips-extend_1d
idea: 058-02.b1_rising-calm-deep-dips-extend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar forward excess return on forecast (forecast < 0, non-overlapping grid): 0.000572981; slope t, day-clustered: 0.607111 (threshold: confirm: slope t >= 2 with supporting check passing; reject: slope t <= -2)
- Supporting check: deepest third: mean short-side 5-bar excess return > 0: 0.00844455, passed: True
- Counts: non-overlapping cases: 396, distinct days: 194
- Decided by: Slope t lies between -2 and 2.
- Reading: Rising calm is the detector's own decision (regime 'unknown', i.e. neither veto fired, since the detector's components are not recorded and warm-up bars are absent), the pullback is last_history_value < 0 (price recompute where missing); the slope's t uses a day-clustered sandwich standard error with a G/(G-1) correction; the deepest third is the floor(n/3) cases with the most negative forecast; drift is the coin's mean 5-bar grid return over all its windows; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move -0.44 % (t -0.77, the cases of one day together: 413 days) per case over 5 bars, -0.044 of the coin's usual move (10.60 %); normal drift in its direction -0.63 %, total -1.08 %; 645 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/058-02.b1_rising-calm-deep-dips-extend_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02.b1_rising-calm-deep-dips-extend_1d`
Measure: `measure.py`

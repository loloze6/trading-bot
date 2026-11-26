---
plan: 058-02_choppy-agitated-weekly-fall-continues_1d
idea: 058-02_choppy-agitated-weekly-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 7-bar move per case: -0.000905795; t of the mean, cases of one day together: -0.0931378 (threshold: confirm: mean > 0 with day-clustered t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger minus smaller |forecast| half: -0.0187925, passed: False
- Counts: cases: 209, days: 168
- Decided by: the t lies between -2 and 2 (or the mean's sign disagrees with it)
- Reading: profile = regime 'unknown', fall = raw scaled 7-day return < 0; a case is the first short bet (rise of |forecast| on the short side >= 2 from its low since the last bet) in each 7-bar grid cell of a window; t uses day-clustered errors (deviations summed per UTC day, G/(G-1) correction); the larger half is |forecast| strictly above the median, the smaller half at or below it; the plan's 30-case minimum gives 'not observable'.
- Size: unusual move -0.09 % (t -0.09, the cases of one day together: 168 days) per case over 7 bars, 0.001 of the coin's usual move (12.44 %); normal drift in its direction -0.96 %, total -1.05 %; 209 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/058-02_choppy-agitated-weekly-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/058-02_choppy-agitated-weekly-fall-continues_1d`
Measure: `measure.py`

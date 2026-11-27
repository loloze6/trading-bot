---
plan: 074-02.b1.b1_calm-stretch-falls-more-coins_1d
idea: 074-02.b1.b1_calm-stretch-falls-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per case, short direction: 0.00844469; t of the mean, cases of one day summed: 2.18231 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: deeper half minus shallower half mean unusual move (split at median |forecast|): -0.00162037, passed: False
- Counts: cases: 1888, distinct days with cases: 753, active bars: 9063
- Decided by: t >= 2 but the supporting check (deeper half minus shallower half > 0) fails, which the plan calls inconclusive.
- Reading: The calm profile is read as regime 'unknown' (no chop veto); a case is the first short bet (rise of short forecast size by >= 2 from its low since the last bet) in each 5-bar grid cell from the window's first row; the normal drift is the coin's mean 5-bar return on that grid over all its windows; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the deeper half is |forecast| strictly above the median, the shallower half at or below it; the plan's '<30 distinct days' rule is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.84 % (t 2.18, the cases of one day together: 753 days) per case over 5 bars, 0.074 of the coin's usual move (11.68 %); normal drift in its direction -0.68 %, total +0.16 %; 1888 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/074-02.b1.b1_calm-stretch-falls-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-02.b1.b1_calm-stretch-falls-more-coins_1d`
Measure: `measure.py`

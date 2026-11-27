---
plan: 061-01_falling-calm-rally-fade_1d
idea: 061-01_falling-calm-rally-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move of short cases (drift removed, short direction): -0.0009079; t of the mean, cases of one day pooled: -0.597313 (threshold: confirm: mean > 0 with day-pooled t >= 2 (and size split > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half: -0.00142648, passed: False
- Counts: cases: 2032, distinct days: 764
- Decided by: Inconclusive rule: the t of the mean unusual move is between -2 and 2.
- Reading: Profile read from the recorded regime ('unknown' = falling calm, not vetoed to chop) and the up day from the raw scaled_rise > 0; cases are short-side bets per the holding rule (a rise of |forecast| >= 2 from its lowest short level since the last bet, reset at flat/long) on every bar (1-bar grid); drift is the coin's mean 1-bar return pooled over all its windows; t uses day-clustered standard error (deviations summed per UTC day); the larger half is |forecast| strictly above the median, the smaller half at or below it.
- Size: unusual move -0.09 % (t -0.60, the cases of one day together: 764 days) per case over 1 bars, -0.014 of the coin's usual move (5.33 %); normal drift in its direction -0.12 %, total -0.21 %; 2032 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/061-01_falling-calm-rally-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/061-01_falling-calm-rally-fade_1d`
Measure: `measure.py`

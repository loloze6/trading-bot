---
plan: 067-01.b1.g1.b1.d1.d1_agitated-chop-slide-continues_1d
idea: 067-01.b1.g1.b1.d1.d1_agitated-chop-slide-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move of short bets, before costs, in the short direction: 0.0136135; t of the mean, cases of one day taken together: 1.51044 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: deeper-fall half minus shallower half, mean unusual move: 0.000710478, passed: True
- Counts: cases: 310, distinct days: 227
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The profile is read from the recorded regime ('unknown' = the choppy agitated profile, the only regime with a strategy) since its 365-bar volatility percentile cannot be rebuilt from the windows, the 30-day fall from last_history_value (or close/close[-30]-1 where missing); a case is the first short bet in each 10-bar grid cell of a window, the deeper half is |forecast| strictly above the median, the day-clustered t uses a G/(G-1) correction, and 'fewer than 30 cases on fewer than 20 distinct days' is read as two minimums (30 cases and 20 distinct days), either one unmet giving 'not observable'.
- Size: unusual move +1.36 % (t 1.51, the cases of one day together: 227 days) per case over 10 bars, 0.055 of the coin's usual move (15.92 %); normal drift in its direction -1.30 %, total +0.07 %; 310 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.d1.d1_agitated-chop-slide-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.d1.d1_agitated-chop-slide-continues_1d`
Measure: `measure.py`

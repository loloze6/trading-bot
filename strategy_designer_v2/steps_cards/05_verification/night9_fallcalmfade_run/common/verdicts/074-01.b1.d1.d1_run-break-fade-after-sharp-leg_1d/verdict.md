---
plan: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d
idea: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg
fit: exact
status: confirmed
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual next-day move of bars with forecast below -2: 0.00547987; t of the mean, cases of one day pooled: 2.08374 (threshold: confirm: mean > 0 with day-pooled t >= 2; reject: t <= -2)
- Supporting check: mean unusual move of top half minus bottom half by |forecast|: 0.00673592, passed: True
- Counts: cases: 2143, distinct days: 621
- Decided by: The mean short-side unusual move is above 0 with a t of 2 or more and the supporting check passes.
- Reading: Falling market read as the 60-bar close change below -10 % and the situation as an up close after at least 2 consecutive down closes, both from closes inside each window, with active bars whose 60-bar or 3-bar history is not in the window left out of the agreement; the top half of the split is |forecast| above the median and the bottom half the rest; the day-pooled t uses per-day summed deviations with a D/(D-1) correction; the plan's 50 cases / 50 days minimum is reported as not observable.
- Size: unusual move +0.55 % (t 2.09, the cases of one day together: 621 days) per case over 1 bars, 0.106 of the coin's usual move (5.44 %); normal drift in its direction -0.13 %, total +0.42 %; 2143 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/common/backtests/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d`
Measure: `measure.py`

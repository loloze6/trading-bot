---
plan: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d
idea: 074-01.b1.d1.d1_run-break-fade-after-sharp-leg
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual next-day move of bars with forecast below -2: -0.00189196; t of the mean, cases of one day pooled: -0.495367 (threshold: confirm: mean > 0 with day-pooled t >= 2; reject: t <= -2)
- Supporting check: mean unusual move of top half minus bottom half by |forecast|: 0.0071568, passed: True
- Counts: cases: 75, distinct days: 38
- Decided by: The plan's minimum of 50 cases on 50 distinct days is not reached (75 cases, 38 days).
- Reading: Falling market read as the 60-bar close change below -10 % and the situation as an up close after at least 2 consecutive down closes, both from closes inside each window, with active bars whose 60-bar or 3-bar history is not in the window left out of the agreement; the top half of the split is |forecast| above the median and the bottom half the rest; the day-pooled t uses per-day summed deviations with a D/(D-1) correction; the plan's 50 cases / 50 days minimum is reported as not observable.
- Size: unusual move -0.19 % (t -0.50, the cases of one day together: 38 days) per case over 1 bars, -0.031 of the coin's usual move (3.33 %); normal drift in its direction +0.02 %, total -0.17 %; 75 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2026/backtests/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d`
Measure: `measure.py`

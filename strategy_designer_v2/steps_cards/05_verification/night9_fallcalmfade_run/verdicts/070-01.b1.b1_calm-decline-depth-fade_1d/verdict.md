---
plan: 070-01.b1.b1_calm-decline-depth-fade_1d
idea: 070-01.b1.b1_calm-decline-depth-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual next-day move on cases: 0.00341635; t of the mean, cases clustered by day: 1.60191 (threshold: positive with t >= 2 (confirm), negative with t <= -2 (reject))
- Supporting check: deeper-minus-shallower mean unusual move (split at median |forecast|): 0.00712156, passed: True
- Counts: distinct case days: 391, cases: 901, deeper half cases: 450, shallower half cases: 451
- Decided by: The main measure's t is between -2 and 2, or the main confirm comes with a deeper-minus-shallower difference at or below 0 with Welch t above -2.
- Reading: Situation recomputed from closes (an up close after at least two lower closes, the run_loss raw value standing in on the first three bars of a window) and the falling calm profile read from regime == mean_reversion since the profile components are not recorded and need more history than a window; cases are short-side forecast rises of at least 2 points per the holding-period bet definition; t clusters cases by UTC day with a D/(D-1) factor; deeper half is |forecast| strictly above the median, shallower at or below; fewer than 30 case days is reported as not observable per the workflow.
- Size: unusual move +0.34 % (t 1.60, the cases of one day together: 391 days) per case over 1 bars, 0.075 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.22 %; 901 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.b1.b1_calm-decline-depth-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.b1.b1_calm-decline-depth-fade_1d`
Measure: `measure.py`

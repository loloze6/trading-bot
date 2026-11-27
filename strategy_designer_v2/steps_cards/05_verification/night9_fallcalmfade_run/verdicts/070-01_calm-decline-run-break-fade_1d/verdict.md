---
plan: 070-01_calm-decline-run-break-fade_1d
idea: 070-01_calm-decline-run-break-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move on short cases (short direction, minus coin mean daily return): 0.00200413; t of the mean, cases summed per day: 0.981443 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: unusual move, run >= 3 minus run 1-2 (Welch t): 0.00642009, passed: True
- Counts: case-days in total: 870, case-days with run >= 3: 236, case-days with run 1-2: 634, distinct days with cases: 488
- Decided by: Inconclusive rule: the main t is between -2 and 2 (or undefined) and no reject rule is met.
- Reading: Cases are all coin-day bars with forecast below 0 and a next-day close in the same window, each counted as one case-day toward the minimums (100 total, 20 per run group, groups by the recorded run length: >=3 vs 1-2); the falling-calm profile in the situation check is read from the detector's recorded regime (mean_reversion = not vetoed) since its profile components are not recorded; the day-clustered t uses deviations summed per UTC day with a D/(D-1) correction.
- Size: unusual move +0.20 % (t 0.98, the cases of one day together: 488 days) per case over 1 bars, 0.044 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.07 %; 870 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01_calm-decline-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01_calm-decline-run-break-fade_1d`
Measure: `measure.py`

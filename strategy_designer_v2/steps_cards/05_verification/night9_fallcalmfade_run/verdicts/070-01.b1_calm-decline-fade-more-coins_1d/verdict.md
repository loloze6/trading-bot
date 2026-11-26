---
plan: 070-01.b1_calm-decline-fade-more-coins_1d
idea: 070-01.b1_calm-decline-fade-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day return beyond the coin's drift, short direction, on forecast<0 bars: 0.000385327; t of the mean, cases summed per day: 0.239169 (threshold: above 0 with t >= 2 confirms; below 0 with t <= -2 rejects)
- Supporting check: next-day excess return, runs >=3 minus runs 1-2 (Welch t -2.143): -0.00445571, passed: True
- Counts: cases: 1667, distinct days: 658, cases with runs of 3 or more: 469, cases with runs of 1 to 2: 1198
- Decided by: Inconclusive: the main t lies between -2 and 2.
- Reading: The falling-calm profile is read from the recorded regime ('mean_reversion' means both vetoes passed) since its components are not recorded, the run length from run_len's last_history_value (logit of the sigmoid) or from closes inside the window; the main mean is over cases with a t whose deviations are summed per day; the supporting check uses the unflipped excess return; 'fewer than 150 cases on fewer than 80 days' is read as two minimum counts, either one missed making the result not observable.
- Size: unusual move +0.04 % (t 0.24, the cases of one day together: 658 days) per case over 1 bars, 0.011 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total -0.09 %; 1667 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.b1_calm-decline-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.b1_calm-decline-fade-more-coins_1d`
Measure: `measure.py`

---
plan: 074-01_falling-market-run-break-fade_1d
idea: 074-01_falling-market-run-break-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side next-day move minus coin drift: 0.00921947; day-clustered t: 3.53551 (threshold: confirm: positive with day-clustered t >= 2 and check passes; reject: t <= -2)
- Supporting check: mean after runs >= 3 minus mean after runs == 2: -0.00474009, passed: False
- Counts: cases: 834, distinct days: 426, cases run >= 3: 428, cases run == 2: 406
- Decided by: Confirming t but the supporting check failed, so neither confirm nor reject.
- Reading: Falling profile recomputed as the 60-bar close change in percent below -10 (the detector's regime veto where 60 window bars are lacking), run length from run_len.last_history_value or recomputed from closes, t clustered by summing deviations per UTC day with a G/(G-1) correction, and the plan's 'at least 30 cases on distinct days' read as the minimum count.
- Size: unusual move +0.92 % (t 3.54, the cases of one day together: 426 days) per case over 1 bars, 0.191 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.80 %; 834 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01_falling-market-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01_falling-market-run-break-fade_1d`
Measure: `measure.py`

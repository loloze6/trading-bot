---
plan: 070-01_falling-calm-run-break-fade_1d
idea: 070-01_falling-calm-run-break-fade
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day return beyond the coin's mean daily return, short direction: -0.000345037; t of the mean, cases of one day summed: -0.181739 (threshold: confirm: mean > 0 with t >= 2; reject: t <= -2)
- Supporting check: mean excess return of runs >= 3 days minus runs of 2 days (Welch t -0.340): -0.001058, passed: True
- Counts: cases: 412, distinct days: 275, cases run >= 3: 216, cases run == 2: 196
- Decided by: Inconclusive: the main t lies between -2 and 2 and no reject rule is met. No effect (common/verdicts.md): t in the idea's direction -0.182 (below 1), 196 cases (30 needed).
- Reading: Falling calm profile read from regime == 'mean_reversion' (the detector's profile vetoes are not recorded), run length from run_len's last_history_value (prices as fallback), cases are all bars with forecast < 0 and a next close in the window, the day-clustered t uses per-day sums of deviations with a D/(D-1) correction, the supporting excess is unsigned (return minus coin mean), and the plan's minimum counts lead to 'not observable' as the workflow requires.
- Size: unusual move -0.03 % (t -0.18, the cases of one day together: 275 days) per case over 1 bars, 0.001 of the coin's usual move (4.55 %); normal drift in its direction -0.09 %, total -0.13 %; 412 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.182 (below 1), 196 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/070-01_falling-calm-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/070-01_falling-calm-run-break-fade_1d`
Measure: `measure.py`

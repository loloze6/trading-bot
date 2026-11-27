---
plan: 074-01.b1.g1_width-times-low-close-rebound_1d
idea: 074-01.b1.g1_width-times-low-close-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-bar return of cases with forecast > 0 (vs coin's all-window mean daily return): 0.00979202; t of the mean, cases grouped by day: 2.2342 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean excess above median forecast minus at/below median: None, passed: False
- Counts: distinct days with cases: 138, cases: 231
- Decided by: The mean excess return is above 0 with t >= 2 but the supporting check fails.
- Reading: Situation checked from prices as range/close over the ddof-1 std of the last 30 in-window daily returns (current bar included) >= 2 and (high-close)/(high-low) >= 0.8 with a long forecast, on the active bars where 30 prior returns exist in the window (the rising-calm profile, needing 60/365-bar histories, is not recomputed); t groups cases per UTC day by summing their deviations; the 30-day minimum is reported as not observable; cases with the median forecast go to the lower group.
- Size: unusual move +1.07 % (t 2.48, the cases of one day together: 134 days) per case over 1 bars, 0.210 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +1.21 %; 221 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/074-01.b1.g1_width-times-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01.b1.g1_width-times-low-close-rebound_1d`
Measure: `measure.py`

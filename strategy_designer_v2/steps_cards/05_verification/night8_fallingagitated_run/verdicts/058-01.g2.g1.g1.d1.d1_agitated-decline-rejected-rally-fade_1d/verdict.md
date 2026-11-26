---
plan: 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d
idea: 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-removed next-day short-side move on case bars: 0.00976566; t of the mean, cases of one day taken together: 3.3828 (threshold: confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean move |forecast| above median minus at or below median: 0.00182778, passed: True
- Counts: case-days: 743, distinct days with cases: 380
- Decided by: Mean drift-removed short-side move is above 0 with t >= 2 and the supporting difference is above 0.
- Reading: The falling-agitated profile is read from the recorded regime (mean_reversion is only reached when neither profile veto fires) since the detector's components are not recorded, the up streak of exactly 1 is recomputed from closes inside each window (first two bars of a window left out of the agreement), and the plan's 'fewer than 30 case-days' is counted as case bars (coin-days) across all coins and windows, treated as a minimum count giving 'not observable'; the day-clustered t sums deviations per UTC day with an n_days/(n_days-1) correction.
- Size: unusual move +1.07 % (t 3.26, the cases of one day together: 301 days) per case over 1 bars, 0.239 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.95 %; 529 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004868 on the check folds against +0.009766 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d`
Measure: `measure.py`

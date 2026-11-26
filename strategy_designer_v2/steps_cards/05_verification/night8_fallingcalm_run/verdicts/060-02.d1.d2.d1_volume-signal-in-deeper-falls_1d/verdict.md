---
plan: 060-02.d1.d2.d1_volume-signal-in-deeper-falls_1d
idea: 060-02.d1.d2.d1_volume-signal-in-deeper-falls
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean signed 5-day excess return: 0.0213505; t of the weighted mean, cases of one day summed: 2.44971 (threshold: confirm if > 0 with t >= 2; reject if < 0 with t <= -2; at least 30 independent days)
- Supporting check: none
- Counts: independent days: 218, cases: 593
- Decided by: Confirm: the weighted mean signed excess return is above 0 with t >= 2 over at least 30 independent days.
- Reading: The 20-day return is computed from closes inside the window when 20 prior bars exist (else the recorded regime 'trending' is taken), the expected side is the sign of ln(30-day mean volume / prior 30-day mean) from volumes when 60 bars exist (else the sign of the raw volfall value); the coin's mean 5-day return is over the non-overlapping grid of all its windows, the t is a ratio-estimator t with weighted deviations summed per UTC day, and fewer than 30 independent days is reported as 'not observable'.
- Size: unusual move +1.89 % (t 3.44, the cases of one day together: 382 days) per case over 5 bars, 0.180 of the coin's usual move (10.60 %); normal drift in its direction -0.11 %, total +1.78 %; 565 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01081 on the check folds against +0.02135 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d1.d2.d1_volume-signal-in-deeper-falls_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d2.d1_volume-signal-in-deeper-falls_1d`
Measure: `measure.py`

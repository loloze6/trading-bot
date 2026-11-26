---
plan: 031-02.b1_deep-fall-still-falling-rebounds_1d
idea: 031-02.b1_deep-fall-still-falling-rebounds
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 30-bar move of long cases (return minus coin's normal 30-bar drift): 0.0450843; day-clustered t: 1.2223 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: Spearman(forecast, excess 30-bar return) on in-regime 30-bar grid bars > 0: -0.0130497, passed: False
- Counts: cases: 140, distinct days: 96, in-regime grid bars: 65
- Decided by: The day-clustered t lies between -2 and 2, so neither the confirm nor the reject rule is met.
- Reading: The 30-day return is recomputed as close[t]/close[t-30]-1 inside the window and active bars where it cannot be computed (first 30 bars) but whose s90 and side agree are left out of the check, s90 is the recorded fall90 raw value (same component and parameters), bets are detected per window starting from a forecast of 0, the first case in each 30-bar grid cell counts, cases without a full 30 bars ahead in their window are dropped, the day-clustered t uses the G/(G-1) correction, in-regime grid bars are those with regime 'mean_reversion', and the plan's 'fewer than 30 cases / fewer than 20 days' are treated as minimum counts giving 'not observable'.
- Size: unusual move +4.51 % (t 1.23, the cases of one day together: 96 days) per case over 30 bars, 0.113 of the coin's usual move (27.67 %); normal drift in its direction +5.01 %, total +9.52 %; 140 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b1_deep-fall-still-falling-rebounds_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1_deep-fall-still-falling-rebounds_1d`
Measure: `measure.py`

---
plan: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (18-bar return minus coin's normal 18-bar drift): 0.00425126; ordinary t of the mean: 3.89869 (threshold: confirm: mean > 0 with ordinary t >= 2.0 and quintile difference > 0; reject: mean < 0 with t <= -2.0)
- Supporting check: mean unusual move of top forecast quintile minus bottom quintile: 0.010326, passed: True
- Counts: independent grid cases: 12156
- Decided by: The main mean is positive with t >= 2.0 and the quintile difference is above 0.
- Reading: Grid cells are positions 0,18,36,... of each window with t+18 inside the window, the coin's drift is the mean of those grid returns over all its windows, quintiles are pooled over all cases by forecast rank, and the plan's 500-case minimum is applied as 'not observable'.
- Size: unusual move +0.18 % per case over 18 bars, 0.019 of the coin's usual move (9.29 %); normal drift in its direction -0.00 %, total +0.18 %; 11344 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h`
Measure: `measure.py`

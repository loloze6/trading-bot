---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean position-weighted 2-bar excess return after weekend fall: 0.00447563; ordinary t of the mean: 2.93532 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 100 cases)
- Supporting check: OLS slope of excess 2-bar return on forecast: 0.000822845, passed: True
- Counts: cases: 2664, active bars: 2711
- Decided by: Mean position-weighted excess return is positive with t >= 2 and the regression slope is above 0.
- Reading: Cases are all bars whose coming bar is Monday with forecast > 0 and close[t+2] in the same window (one per coin per week by construction), the coin mean daily return is pooled over all its windows, the slope is an OLS of the unweighted excess 2-bar return on forecast, and the plan's 'fewer than 100 cases' rule is reported as not observable.
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d`
Measure: `measure.py`

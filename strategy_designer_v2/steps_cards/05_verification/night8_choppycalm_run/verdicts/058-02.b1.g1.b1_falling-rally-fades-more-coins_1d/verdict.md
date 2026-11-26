---
plan: 058-02.b1.g1.b1_falling-rally-fades-more-coins_1d
idea: 058-02.b1.g1.b1_falling-rally-fades-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean excess next-bar return on forecast<0 bars: -0.00248643; day-clustered t of weighted mean: -1.47398 (threshold: negative with t <= -2 confirms (with slope < 0); positive with t >= +2 rejects; 100 cases over 60 days minimum)
- Supporting check: OLS slope of excess next-bar return on abs(forecast) below 0: 2.52044e-05, passed: False
- Counts: cases: 6519, distinct days: 1426
- Decided by: Inconclusive: the t lies between -2 and +2.
- Reading: Falling profile read from the recorded regime 'unknown' (the detector's 60-bar trend is not recorded); the situation is raw scaled_rise > 0 in that regime, expected side short; the day-clustered t uses per-day sums of w*(excess - weighted mean) over sum(w) with a D/(D-1) correction; days are UTC dates of the case bar.
- Size: unusual move +0.27 % (t 1.62, the cases of one day together: 1134 days) per case over 1 bars, 0.051 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.11 %; 4364 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b1_falling-rally-fades-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b1_falling-rally-fades-more-coins_1d`
Measure: `measure.py`

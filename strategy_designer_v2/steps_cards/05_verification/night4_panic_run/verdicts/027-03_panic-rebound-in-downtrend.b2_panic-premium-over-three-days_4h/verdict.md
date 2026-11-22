---
plan: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
fit: adapted
status: inconclusive
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 18-bar return of bets over the coin's mean 18-bar return: 0.0364656; t of the mean: 5.03601 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean excess above median forecast minus below median: -0.0276736, passed: False
- Counts: independent cases: 135
- Decided by: t >= 2 but the supporting check fails, which the plan calls inconclusive.
- Reading: Situation recomputed from prices (6-bar return over the mean absolute 6-bar return of the last 180 bars, bar range as (high-low)/close, recorded range_excess raw value used where present, partial windows from 30 bars, 5% tolerance, active bars whose situation cannot be computed left out); cases are the first bet in each 18-bar cell of each window's grid from its first row with the 18-bar return inside the window, the coin mean is over the non-overlapping 18-bar grid of all its windows, excess is not sign-flipped (all bets are long by plan), and the median split uses cases strictly above versus strictly below the median forecast.
- Size: unusual move +3.65 % per case over 18 bars, 0.424 of the coin's usual move (8.17 %); normal drift in its direction +0.42 %, total +4.07 %; 135 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h`
Measure: `measure.py`

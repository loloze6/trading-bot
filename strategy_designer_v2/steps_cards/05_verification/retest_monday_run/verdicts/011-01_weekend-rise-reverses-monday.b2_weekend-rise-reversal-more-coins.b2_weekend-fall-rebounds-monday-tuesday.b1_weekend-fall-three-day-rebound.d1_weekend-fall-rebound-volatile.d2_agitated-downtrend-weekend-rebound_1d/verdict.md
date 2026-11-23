---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d2_agitated-downtrend-weekend-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d2_agitated-downtrend-weekend-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 3-day return of Sunday cases (forecast >= 2): 0.0240589; t of the forecast-weighted mean: 5.88407 (threshold: confirm: mean > 0 with t >= 2 and supporting check; reject: mean < 0 with t <= -2; at least 100 cases)
- Supporting check: mean excess return, top half minus bottom half of forecast: 0.0199413, passed: True
- Counts: cases: 1144
- Decided by: The forecast-weighted mean excess 3-day return is positive with t >= 2 and the top-half minus bottom-half difference is above 0.
- Reading: Sunday bars are those whose bar start (UTC) is a Sunday; the 20-day return is close[t]/close[t-20]-1 inside the window (the recorded regime where 20 prior bars are not in the window); the weekend fall is the raw component < 0 (else Sunday's close-to-close return); the weighted t uses the heteroskedasticity-robust standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); top and bottom halves are the upper and lower n//2 cases by forecast (stable sort, middle case dropped if n is odd), compared by unweighted means; the plan's fewer-than-100-cases rule is applied as a minimum count (not observable).
- Size: unusual move +1.68 % per case over 3 bars, 0.192 of the coin's usual move (9.14 %); normal drift in its direction +0.46 %, total +2.14 %; 1145 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d2_agitated-downtrend-weekend-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d2_agitated-downtrend-weekend-rebound_1d`
Measure: `measure.py`

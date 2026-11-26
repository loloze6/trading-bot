---
plan: 058-02.b1.g1_falling-market-rally-fades_1d
idea: 058-02.b1.g1_falling-market-rally-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean next-day unusual move, short direction: 0.00273454; t of weighted mean, cases of one day pooled: 1.50851 (threshold: positive with t >= 2 to confirm; negative with t <= -2 to reject)
- Supporting check: unusual move above-median minus at-or-below-median abs(forecast) (Welch t -0.913): -0.00156966, passed: False
- Counts: distinct days carrying cases: 1126, cases: 2951
- Decided by: The main t lies between -2 and 2.
- Reading: Falling profile taken from the recorded regime ('unknown' = not vetoed to 'chop'), plus a negative 60-bar close change where computable inside the window; next-day return minus the coin's mean daily return over all its windows, sign-flipped for the short; the weighted mean's t uses day-clustered standard errors (weighted deviations summed per UTC day, small-sample factor K/(K-1)); the supporting check uses unweighted group means of the unusual move with Welch's t; fewer than 30 distinct days is treated as a minimum count not reached (not observable).
- Size: unusual move +0.30 % (t 1.68, the cases of one day together: 861 days) per case over 1 bars, 0.066 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.18 %; 1962 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1_falling-market-rally-fades_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1_falling-market-rally-fades_1d`
Measure: `measure.py`

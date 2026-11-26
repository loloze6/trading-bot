---
plan: 058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation_1d
idea: 058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean of sign(forecast) x (5-bar return minus coin's mean 5-bar return): 0.00744639; t of weighted mean, cases of one day pooled: 1.70788 (threshold: confirm: > 0 with t >= 2 and convexity check passes; reject: < 0 with t <= -2)
- Supporting check: upper-minus-lower half mean signed excess return per unit |raw position|: 0.000502058, passed: True
- Counts: grid cases: 3435, distinct days: 506
- Decided by: The t is between -2 and 2 (or sign and t disagree), which the plan calls inconclusive.
- Reading: Grid at positions 0,5,10,... of each window with cases where forecast != 0; coin mean 5-bar return taken over that same grid on all its windows; t is cluster-robust by calendar day; halves split at the median |raw| (ties to the lower half) and 'per unit' is the half's mean signed excess return (unweighted) divided by its mean |raw|; calm is regime not 'chop'.
- Size: unusual move +0.75 % (t 2.59, the cases of one day together: 1292 days) per case over 5 bars, 0.067 of the coin's usual move (11.68 %); normal drift in its direction -0.01 %, total +0.74 %; 3061 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation_1d`
Measure: `measure.py`

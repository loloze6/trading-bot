---
plan: 059-01.b1_calm-decline-all-coins_1d
idea: 059-01.b1_calm-decline-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean short drift-removed 5-day return: 0.00529676; t of weighted mean, cases of a day grouped: 0.861926 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 30 distinct days)
- Supporting check: deeper-half minus shallower-half mean drift-removed 5-day return (must be < 0): 0.00094252, passed: False
- Counts: distinct days: 379, cases: 1739
- Decided by: The t lies between -2 and 2.
- Reading: Calm market = bars whose regime is 'unknown' (not vetoed to 'chop'), the situation is calm and raw component < 0 (recomputed from closes where not recorded), side short; cases are forecast<0 bars on the 0,5,10,... grid of each window with a 5-bar return inside the window, drift is the coin's mean 5-bar return over all its grid bars, the t is the weighted mean over a day-clustered standard error (weighted deviations summed per day), and the halves split at the median |forecast| (deeper: strictly above), compared on unweighted means of the unsigned drift-removed return.
- Size: unusual move +0.99 % (t 2.66, the cases of one day together: 768 days) per case over 5 bars, 0.089 of the coin's usual move (11.68 %); normal drift in its direction -0.68 %, total +0.31 %; 1861 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/059-01.b1_calm-decline-all-coins_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-01.b1_calm-decline-all-coins_1d`
Measure: `measure.py`

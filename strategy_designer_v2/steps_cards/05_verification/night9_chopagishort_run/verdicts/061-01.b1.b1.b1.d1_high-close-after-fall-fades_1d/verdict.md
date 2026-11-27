---
plan: 061-01.b1.b1.b1.d1_high-close-after-fall-fades_1d
idea: 061-01.b1.b1.b1.d1_high-close-after-fall-fades
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per short bet, in the short direction: 0.0253697; t of the mean, cases grouped by day: 3.80481 (threshold: confirm: a fall with t >= 2; reject: a rise with t <= -2; over at least 30 cases on at least 20 days)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half (>= 0): 0.00471781, passed: True
- Counts: cases: 190, days: 157
- Decided by: The mean unusual move is a fall with t >= 2 over at least 30 cases on 20 days, and the supporting check passes.
- Reading: Profile taken from the regime column (bars not vetoed to 'chop') since its components are not recorded; the 5-day return and close location from the recorded fall5/highclose raw values, else from prices; cases are short bets only, first bet per 5-bar cell; day-clustered t with G/(G-1) correction; the |forecast| halves are the lower and upper n//2 cases by rank (middle case dropped when odd).
- Size: unusual move +2.54 % (t 3.82, the cases of one day together: 157 days) per case over 5 bars, 0.217 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.89 %; 190 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01582 on the check folds against +0.02537 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1_high-close-after-fall-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1_high-close-after-fall-fades_1d`
Measure: `measure.py`

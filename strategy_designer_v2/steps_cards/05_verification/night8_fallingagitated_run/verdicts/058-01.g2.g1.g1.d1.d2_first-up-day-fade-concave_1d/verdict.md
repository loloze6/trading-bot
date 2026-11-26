---
plan: 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d
idea: 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day fall on case bars, summed per day: 0.0185018; t of the mean across days: 3.19895 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 100 case-days)
- Supporting check: mean unusual fall, |forecast| above median minus below median: 0.00660079, passed: True
- Counts: case-days: 387, cases: 759, active bars: 742
- Decided by: Mean unusual fall above 0 with t >= 2 and the high-|forecast| minus low-|forecast| difference above 0.
- Reading: The falling-agitated profile is taken from the recorded regime (its detector components are not recorded and their 365-bar lookback cannot be rebuilt inside a window) while the streak of exactly 1 is recomputed from closes (first two bars of each window left out); the supporting check splits individual cases strictly above and below the cases' median |forecast|, cases equal to it left out.
- Size: unusual move +0.93 % (t 3.20, the cases of one day together: 384 days) per case over 1 bars, 0.202 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.81 %; 753 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.008573 on the check folds against +0.0185 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d`
Measure: `measure.py`

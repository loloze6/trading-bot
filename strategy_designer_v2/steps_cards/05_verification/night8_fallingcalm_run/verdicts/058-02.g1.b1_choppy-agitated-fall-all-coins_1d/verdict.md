---
plan: 058-02.g1.b1_choppy-agitated-fall-all-coins_1d
idea: 058-02.g1.b1_choppy-agitated-fall-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean short-direction 5-bar excess return: 0.0186653; day-pooled t of the weighted mean: 1.55139 (threshold: above 0 with day-pooled t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: mean short-direction excess return, top third minus bottom third of |forecast|: 0.0107239, passed: True
- Counts: cases: 266, distinct days: 141
- Decided by: Inconclusive: the day-pooled t lies between -2 and 2.
- Reading: Situation: raw fall_depth < 0 on a non-'chop' regime bar, short side; cases are grid bars 0,5,10,... of each window with a full 5-bar return inside it; the coin's mean 5-bar return is the mean over the same grid of all its windows; the day-pooled t uses the weighted mean's deviations (weight x (value - mean)) summed per UTC day with a D/(D-1) correction; thirds are the floor(n/3) cases with the smallest and the largest |forecast|, compared by their unweighted means.
- Size: unusual move +0.94 % (t 1.64, the cases of one day together: 297 days) per case over 5 bars, 0.072 of the coin's usual move (11.38 %); normal drift in its direction -0.69 %, total +0.25 %; 410 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-02.g1.b1_choppy-agitated-fall-all-coins_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-02.g1.b1_choppy-agitated-fall-all-coins_1d`
Measure: `measure.py`

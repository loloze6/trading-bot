---
plan: 074-01.b1.b1.b1_falling-widest-up-day-fade_1d
idea: 074-01.b1.b1.b1_falling-widest-up-day-fade
fit: adapted
status: inconclusive
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction next-bar unusual move (return minus drift): 0.00472924; t of the mean, cases summed per day: 1.17784 (threshold: mean > 0 with t >= 2 confirms (with wider half beating narrower half); t <= -2 rejects)
- Supporting check: wider-half minus narrower-half mean unusual move (median split of range_multiple): 0.00853803, passed: True
- Counts: cases: 893, distinct days: 416
- Decided by: The t lies between -2 and 2 (or the mean is not above 0), meeting neither the confirm nor the reject rule.
- Reading: Situation computed as close above prior close with range multiple >= 1 (recorded value where present, else recomputed), bars where it cannot be computed left out of the agreement; cases are short bets (forecast rising >= 2 points on the short side) on mean_reversion bars with a next bar in the window; the wider half is cases above the median range multiple, the narrower half at or below it; fewer than the plan's minimum counts is reported as not observable.
- Size: unusual move +0.47 % (t 1.18, the cases of one day together: 416 days) per case over 1 bars, 0.092 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.32 %; 893 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1_falling-widest-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1_falling-widest-up-day-fade_1d`
Measure: `measure.py`

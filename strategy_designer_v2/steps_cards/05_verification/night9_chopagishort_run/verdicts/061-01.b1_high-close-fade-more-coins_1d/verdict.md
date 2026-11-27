---
plan: 061-01.b1_high-close-fade-more-coins_1d
idea: 061-01.b1_high-close-fade-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar fall per short case (drift removed, sign flipped): 0.00640957; t of the mean, cases clustered by day: 1.73898 (threshold: mean unusual fall > 0 with t >= 2 confirms (with upper-minus-lower > 0); < 0 with t <= -2 rejects)
- Supporting check: upper-half minus lower-half mean unusual fall, split at median close location: -0.00314687, passed: False
- Counts: cases: 411, distinct days: 283
- Decided by: The t of the mean unusual fall lies between -2 and 2 (inconclusive rule).
- Reading: The choppy-agitated profile is taken from the recorded regime (mean_reversion is only reached when no chop veto fires, since the detector's trend and volatility components are not recorded and their warm-up is not in the record) together with the close location >= 0.8 from the prices and the short side; a case is the first short bet (forecast rise of >= 2 points on the short side from its lowest level since the last bet) in each non-overlapping 2-bar grid cell of a window, its return taken from that bar's close 2 bars ahead in the same window; the median split puts cases above the median close location in the upper half; the t clusters cases by UTC day with a G/(G-1) correction; fewer than the plan's minimum counts is reported as not observable.
- Size: unusual move +0.64 % (t 1.74, the cases of one day together: 283 days) per case over 2 bars, 0.110 of the coin's usual move (7.35 %); normal drift in its direction -0.26 %, total +0.39 %; 411 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1_high-close-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1_high-close-fade-more-coins_1d`
Measure: `measure.py`

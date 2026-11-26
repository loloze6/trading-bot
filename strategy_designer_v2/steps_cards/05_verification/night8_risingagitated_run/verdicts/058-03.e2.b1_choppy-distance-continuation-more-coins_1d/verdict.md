---
plan: 058-03.e2.b1_choppy-distance-continuation-more-coins_1d
idea: 058-03.e2.b1_choppy-distance-continuation-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (10-bar return - coin drift): 0.0118982; t of the mean, cases summed per date: 0.97301 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: Welch t of signed excess return, |forecast| above minus below median: 1.44904, passed: True
- Counts: cases: 817, distinct dates: 212
- Decided by: The main measure's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are grid bars (positions 0,10,20,... of each window) with forecast != 0 and a full 10-bar forward return in the window, drift is the coin's mean 10-bar return on that grid over all its windows, the t uses per-date summed deviations from the mean (clustered SE with J/(J-1) correction), and the median split puts |forecast| > median above and <= median below.
- Size: unusual move +0.67 % (t 1.08, the cases of one day together: 808 days) per case over 10 bars, 0.014 of the coin's usual move (16.82 %); normal drift in its direction -0.01 %, total +0.66 %; 1495 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-03.e2.b1_choppy-distance-continuation-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03.e2.b1_choppy-distance-continuation-more-coins_1d`
Measure: `measure.py`

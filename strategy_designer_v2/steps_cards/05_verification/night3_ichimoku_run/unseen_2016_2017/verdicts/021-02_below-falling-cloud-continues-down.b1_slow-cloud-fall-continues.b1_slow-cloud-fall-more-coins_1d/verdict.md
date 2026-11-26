---
plan: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d
idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (26-bar forward return - coin's 26-bar drift) on trending grid bars: 0.0776219; t of the mean: 1.30189 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: slow-fall half minus fast-fall half excess 26-bar return (split at median slow_fall), Welch t: -0.174584, passed: True
- Counts: independent grid cases in the regime: 8, slow-fall half: 4, fast-fall half: 4
- Decided by: A minimum count is not reached: the plan needs at least 30 independent grid cases in the regime and at least 15 per half.
- Reading: Situation recomputed from each window's own prices (Ichimoku 9/26/52/26, close below the lower cloud edge and cloud mid 26-bar percent slope < 0) where enough history exists, and taken from the recorded regime 'trending' (the detector's rule of those two conditions) on bars where it cannot be recomputed; the slower-fall half is slow_fall above its median (larger 1/(1+fall%)), the faster half at or below it; drift is the coin's mean non-overlapping 26-bar return over all its windows; the plan's 'fewer than 30 cases or 15 per half' is treated as the minimum-count rule giving 'not observable'.
- Size: unusual move +4.65 % (t 0.40, the cases of one day together: 15 days) per case over 26 bars, 0.084 of the coin's usual move (67.63 %); normal drift in its direction -30.38 %, total -25.73 %; 16 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/unseen_2016_2017/backtests/021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d`
Measure: `measure.py`

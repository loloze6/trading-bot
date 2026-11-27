---
plan: 067-02.b1.b1.b2.b1_choppy-downside-stretch-more-coins_1d
idea: 067-02.b1.b1.b2.b1_choppy-downside-stretch-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean short-side 5-day excess move (minus drift), day-pooled t: 0.0079231; t of the weighted mean, same-day cases pooled: 0.950987 (threshold: mean > 0 with t >= 2 confirms (with size check > 0); t <= -2 rejects; else inconclusive)
- Supporting check: mean excess, larger half minus smaller half of |forecast|: -0.00701931, passed: False
- Counts: grid cases: 797, distinct days: 288
- Decided by: The main measure's t lies between -2 and 2 (or its mean is not above 0).
- Reading: The choppy profile is the bars whose regime is 'unknown' (the only regime with a strategy, the vetoes sending |60-bar trend| > 10 to the null 'chop'), below the average is a raw stretch < 0 (recomputed as close < 20-bar SMA where not recorded); the drift is each coin's mean 5-bar return on the window grids; the weighted mean's t pools per-day sums of weighted deviations (cluster SE with D/(D-1)); the size split puts |forecast| > median in the larger half and uses unweighted half means; the plan's minimum counts, if not met, give 'not observable'.
- Size: unusual move +0.88 % (t 2.31, the cases of one day together: 702 days) per case over 5 bars, 0.068 of the coin's usual move (12.35 %); normal drift in its direction -0.79 %, total +0.09 %; 1270 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-02.b1.b1.b2.b1_choppy-downside-stretch-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1.b1.b2.b1_choppy-downside-stretch-more-coins_1d`
Measure: `measure.py`

---
plan: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h
idea: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 18-bar excess return over normal drift, per bet, pooled: 0.00836326; t of the weighted mean: 4.75595 (threshold: positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 over at least 30 cases to reject)
- Supporting check: timing gain: mean daily book return minus position x coin mean daily return: 0.000638866, passed: True
- Counts: cases: 4643
- Decided by: weighted mean excess return positive with t >= 2 over at least 30 cases, and timing gain positive.
- Reading: The down-streak is the run of consecutive closes below the previous close (capped at 180 bars) with the volume slope fitted on those falling bars, the first bet in each 18-bar grid cell is the case, the t of the forecast-weighted mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w), and the daily position for the market part is the mean allocation held over the bars of that day.
- Size: unusual move +0.51 % (t 2.32, the cases of one day together: 1923 days) per case over 18 bars, 0.053 of the coin's usual move (9.37 %); normal drift in its direction +0.71 %, total +1.22 %; 4643 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/common/backtests/024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h`
Measure: `measure.py`

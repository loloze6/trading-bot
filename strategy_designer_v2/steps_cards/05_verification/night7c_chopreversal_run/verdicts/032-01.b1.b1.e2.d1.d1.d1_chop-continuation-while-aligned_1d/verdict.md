---
plan: 032-01.b1.b1.e2.d1.d1.d1_chop-continuation-while-aligned_1d
idea: 032-01.b1.b1.e2.d1.d1.d1_chop-continuation-while-aligned
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of sign(position) x (next-day return - coin mean daily return) on in-regime position bars: 0.00181947; t of the mean, clustered by day: 2.19491 (threshold: confirm: mean > 0 with t >= 2 (and top-minus-bottom difference > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean excess, top half minus bottom half of |forecast| (Welch t -0.501): -0.000559329, passed: False
- Counts: in-regime position-days: 7563, distinct days: 2491
- Decided by: The main measure meets the confirm rule but the top-half minus bottom-half difference is not above 0.
- Reading: Situation recomputed per window from closes (ER = |close[t]-close[t-30]| / sum of 30 absolute daily changes, 30- and 7-day close-to-close returns, side = sign of the 7-day return) and agreement taken over active bars where it is computable (first 30 bars of each window left out); cases are bars with regime 'trending' and a non-zero position, the coin mean is the mean of all its within-window daily returns, the main t is clustered by calendar day (deviations summed per day), and the top half is |forecast| above its median among the cases, the bottom half at or below it.
- Size: unusual move +0.14 % (t 1.26, the cases of one day together: 1764 days) per case over 1 bars, 0.030 of the coin's usual move (4.78 %); normal drift in its direction -0.01 %, total +0.14 %; 3640 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d1.d1_chop-continuation-while-aligned_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d1.d1.d1_chop-continuation-while-aligned_1d`
Measure: `measure.py`

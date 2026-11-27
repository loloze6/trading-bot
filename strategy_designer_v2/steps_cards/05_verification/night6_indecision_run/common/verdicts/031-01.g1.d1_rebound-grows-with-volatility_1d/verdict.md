---
plan: 031-01.g1.d1_rebound-grows-with-volatility_1d
idea: 031-01.g1.d1_rebound-grows-with-volatility
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return on signal bars (day-pooled): 0.0123455; t of the mean, cases of one day pooled: 3.8997 (threshold: confirm: mean > 0 with t >= 2 and high-minus-low > 0; reject: mean < 0 with t <= -2)
- Supporting check: high-minus-low forecast excess return (Welch t 4.125): 0.011576, passed: True
- Counts: cases (signal days): 1932, distinct days: 659, cases above median: 966, cases below median: 966
- Decided by: Mean excess return above 0 with t >= 2 and a high-minus-low difference above 0.
- Reading: The plan's situation is recomputed from prices as range(t)/mean of the last 20 bar ranges including t >= 1.5 and (close-low)/(high-low) <= 0.25, and the agreement is taken over active bars where these are computable (the first 19 bars of each window lack history); 'cases (signal days)' are coin-day signal bars, the t pools a day's cases by summing their deviations (cluster-robust by day), and cases equal to the median forecast are left out of both supporting groups.
- Size: unusual move +1.26 % (t 3.99, the cases of one day together: 635 days) per case over 1 bars, 0.229 of the coin's usual move (5.39 %); normal drift in its direction +0.14 %, total +1.40 %; 1853 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.g1.d1_rebound-grows-with-volatility_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/common/backtests/031-01.g1.d1_rebound-grows-with-volatility_1d`
Measure: `measure.py`

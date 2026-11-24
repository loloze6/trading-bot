---
plan: 031-01.g1.d1_rebound-grows-with-volatility_1d
idea: 031-01.g1.d1_rebound-grows-with-volatility
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return on signal bars (day-pooled): 0.0131423; t of the mean, cases of one day pooled: 1.16566 (threshold: confirm: mean > 0 with t >= 2 and high-minus-low > 0; reject: mean < 0 with t <= -2)
- Supporting check: high-minus-low forecast excess return (Welch t -0.274): -0.00463275, passed: False
- Counts: cases (signal days): 85, distinct days: 58, cases above median: 42, cases below median: 42
- Decided by: The main measure's t lies between -2 and 2 (or cannot be computed).
- Reading: The plan's situation is recomputed from prices as range(t)/mean of the last 20 bar ranges including t >= 1.5 and (close-low)/(high-low) <= 0.25, and the agreement is taken over active bars where these are computable (the first 19 bars of each window lack history); 'cases (signal days)' are coin-day signal bars, the t pools a day's cases by summing their deviations (cluster-robust by day), and cases equal to the median forecast are left out of both supporting groups.
- Size: unusual move +1.41 % (t 1.22, the cases of one day together: 53 days) per case over 1 bars, 0.222 of the coin's usual move (7.81 %); normal drift in its direction +0.98 %, total +2.39 %; 77 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.g1.d1_rebound-grows-with-volatility_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.g1.d1_rebound-grows-with-volatility_1d`
Measure: `measure.py`

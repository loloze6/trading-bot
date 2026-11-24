---
plan: 031-02.b1.b2_failed-rally-more-coins_1d
idea: 031-02.b1.b2_failed-rally-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (20-bar return - coin mean 20-bar return): 0.00309214; t of the mean (cases summed per day): 0.536167 (threshold: confirm: mean > 0 with t >= 2 and supporting check; reject: mean < 0 with t <= -2)
- Supporting check: mean excess 20-bar return on cases with forecast < 0 is below 0: 0.00997247, passed: False
- Counts: cases: 758, distinct days: 116, cases with forecast below 0: 257
- Decided by: The main measure's t lies between -2 and 2 (or its sign disagrees with the mean's).
- Reading: The 60-day return is recomputed from closes inside each window where 60 prior bars exist and taken from the recorded regime otherwise; 'nearer than usual' is the standardised dist_low (post_pipeline_value) below 10; the coin's mean 20-bar return is the mean over the non-overlapping grid returns of all its windows; the main measure's value is the mean product per case and its t is the ordinary t of the per-day sums; per the instructions, fewer than 100 cases or 60 distinct days gives 'not observable'.
- Size: unusual move +2.76 % (t 1.70, the cases of one day together: 353 days) per case over 20 bars, 0.108 of the coin's usual move (23.14 %); normal drift in its direction +0.67 %, total +3.43 %; 522 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-02.b1.b2_failed-rally-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1.b2_failed-rally-more-coins_1d`
Measure: `measure.py`

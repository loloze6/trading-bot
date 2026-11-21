---
plan: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d
idea: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return on Saturday-signal bars: 0.00980304; t of the mean: 6.07818 (threshold: confirm: weighted mean > 0 with t >= 2 and correlation > 0; reject: weighted mean < 0 with t <= -2)
- Supporting check: Pearson correlation of forecast and next-day excess return: 0.118329, passed: True
- Counts: Saturday bars with forecast > 0: 1250, Saturday-signal bars: 2478
- Decided by: The weighted mean excess return is positive with t >= 2 and the correlation is above 0.
- Reading: Situation bars are those whose next day (timestamp + 1 day) is a Saturday with a positive 7-day return (recorded raw value, else recomputed from closes); the t is the ordinary t of the unweighted mean excess return over Saturday-signal bars with forecast > 0, the correlation uses all Saturday-signal bars (regime mean_reversion) with a next-day return, and the plan's minimum of 300 bars is applied as 'not observable'.
- Size: unusual move +0.78 % per case over 1 bars, 0.158 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.90 %; 1069 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d`
Measure: `measure.py`

---
plan: 054-02.b1_reclaim-rebound-all-coins_1d
idea: 054-02.b1_reclaim-rebound-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: 5-day forward return after case bars minus that of the other falling-agitated bars: 0.0152651; Welch t (cases of a day taken together): 0.805681 (threshold: confirm: difference > 0 with Welch t >= 2 (and Spearman > 0); reject: difference < 0 with t <= -2)
- Supporting check: Spearman of reclaim post_pipeline_value vs drift-adjusted 5-day return: -0.108007, passed: False
- Counts: cases: 153, distinct days: 72, other falling-agitated bars: 969
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the difference), meeting neither rule.
- Reading: The falling-agitated profile is taken from the detector's recorded regime (mean_reversion or unknown, i.e. no veto fired) intersected with a 60-day close return below -10 % where the window allows, because the 365-day volatility median cannot be rebuilt inside a ~122-bar window; cases are the first long bet (forecast rise >= 2 from its low since the last bet) in each 5-bar grid cell, others are in-profile grid bars of cells without a case, and the Welch t uses a day-clustered standard error on the case side.
- Size: unusual move +1.76 % (t 0.95, the cases of one day together: 72 days) per case over 5 bars, 0.158 of the coin's usual move (11.68 %); normal drift in its direction +0.72 %, total +2.49 %; 153 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-02.b1_reclaim-rebound-all-coins_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-02.b1_reclaim-rebound-all-coins_1d`
Measure: `measure.py`

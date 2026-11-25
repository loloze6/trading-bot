---
plan: 047-02_falling-agitated-daily-rise-giveback_1d
idea: 047-02_falling-agitated-daily-rise-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast (post_pipeline_value), day-clustered SE: 7.00351e-05; day-clustered t of slope: 0.245678 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean next-day excess return, short direction (negated), > 0: 0.0055899, passed: True
- Counts: cases (bars with forecast < 0): 1326, distinct days: 633
- Decided by: Inconclusive rule: the slope's t lies between -2 and 2.
- Reading: The profile is read from the recorded regime ('unknown' = neither chop veto fired), the one-day rise from last_history_value (prices where missing); cases are bars with forecast < 0 that have a next bar in the same window; the regression has an intercept with CR1 day-clustered standard errors (G/(G-1)*(N-1)/(N-K)); the plan's 'fewer than 100 cases or 50 days' is treated as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +0.60 % (t 2.26, the cases of one day together: 449 days) per case over 1 bars, 0.133 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.47 %; 858 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/047-02_falling-agitated-daily-rise-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/047-02_falling-agitated-daily-rise-giveback_1d`
Measure: `measure.py`

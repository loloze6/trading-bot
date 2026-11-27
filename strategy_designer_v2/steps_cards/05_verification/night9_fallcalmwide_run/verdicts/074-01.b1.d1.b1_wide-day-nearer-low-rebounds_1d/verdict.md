---
plan: 074-01.b1.d1.b1_wide-day-nearer-low-rebounds_1d
idea: 074-01.b1.d1.b1_wide-day-nearer-low-rebounds
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return on forecast>0 bars: 0.00473888; t of the mean, cases of one day summed: 1.70785 (threshold: confirm if mean > 0 with day-clustered t >= 2 and slope check passes; reject if mean < 0 with t <= -2)
- Supporting check: OLS slope of next-day excess return on low_close post_pipeline_value (t >= 1, positive): 0.00210092, passed: True
- Counts: distinct days with cases: 330, cases: 641
- Decided by: The day-clustered t lies between -2 and 2.
- Reading: The rising-calm profile is taken from the recorded regime (not 'chop', since its components are not recorded and its 365-day lookback exceeds a window), range in usual moves is rebuilt from prices with a 30-bar ddof-1 std of in-window daily returns (bars without 30 prior returns are left out of the agreement), close location uses the recorded raw value where present; the main t clusters cases by UTC day (per-day summed deviations, G/(G-1) correction); the 30-day minimum, when unmet, gives 'not observable' per the workflow rule.
- Size: unusual move +0.50 % (t 1.79, the cases of one day together: 305 days) per case over 1 bars, 0.105 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.64 %; 582 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/074-01.b1.d1.b1_wide-day-nearer-low-rebounds_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01.b1.d1.b1_wide-day-nearer-low-rebounds_1d`
Measure: `measure.py`

---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of pooled slope of demeaned forward 168-bar return on forecast (trending grid bars): 3.82623; OLS slope t: 3.82623 (threshold: confirm if t >= 2 and slope positive in >= 4 of 6 coins; reject if t <= -2)
- Supporting check: coins with positive slope (need at least 4 of 6): 5, passed: True
- Counts: independent trending grid bars: 1227, trending grid bars with forecast above 0: 750, coins with positive slope: 5
- Decided by: The slope t is at least 2 and the slope is positive in at least 4 of the 6 coins.
- Reading: Grid bars are positions 0,168,... of each window kept when the recorded regime is trending and the forward return stays inside the window; the coin mean is the mean of its grid 168-bar returns over all windows; the pooled OLS includes an intercept; a coin with no computable slope counts as not positive; the plan's 'inconclusive' for too few cases is reported as 'not observable' per the workflow.
- Size: unusual move +0.50 % per case over 168 bars, 0.033 of the coin's usual move (12.47 %); normal drift in its direction +0.98 %, total +1.48 %; 1191 cases
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h`
Measure: `measure.py`

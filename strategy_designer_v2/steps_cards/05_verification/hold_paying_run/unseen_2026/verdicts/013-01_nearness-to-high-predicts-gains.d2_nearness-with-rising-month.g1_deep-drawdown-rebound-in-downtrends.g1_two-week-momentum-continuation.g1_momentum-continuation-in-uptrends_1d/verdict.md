---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of demeaned 7-bar forward return on forecast (trending, non-overlapping): 0.523947; OLS slope t: 0.523947 (threshold: positive slope with t >= 2 (and positive timing gain) confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: timing gain: book mean daily return before costs minus market-rise part: 0.00075174, passed: True
- Counts: independent 7-bar cases in trending regime: 121, trending cases with forecast above 0: 79
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: The plan's situation is taken as a positive 60-bar return (recomputed from closes inside the window, falling back to the recorded regime where 60 prior bars are missing) with the graded 14-bar rise recorded and a long position, not requiring the 14-bar rise itself to be positive; the coin's mean 7-bar return is the mean over all its 7-bar grid samples in all windows; the timing gain is computed on the book's daily returns before fees (value before the day's trade over the previous value after rebalance).
Plan: `steps_cards/03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/hold_paying_run/unseen_2026/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d`
Measure: `measure.py`

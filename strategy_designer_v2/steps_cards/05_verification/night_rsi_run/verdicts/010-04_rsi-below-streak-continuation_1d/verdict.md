---
plan: 010-04_rsi-below-streak-continuation_1d
idea: 010-04_rsi-below-streak-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 14-bar excess forward return on run length below 50 (grid bars with forecast < 0): 0.00105054; OLS slope t: 1.28455 (threshold: confirm if slope < 0 with t <= -2 and supporting check passes; reject if slope > 0 with t >= +2; else inconclusive)
- Supporting check: mean 14-bar gain before costs: position x (14-bar return - coin mean 14-bar return), > 0: -0.000119349, passed: False
- Counts: independent grid cases with forecast < 0: 185, grid cases with forecast < 0, BTCUSD: 89, grid cases with forecast < 0, ETHUSD: 96, grid cases in supporting check: 185
- Decided by: The slope's t lies between -2 and +2 (inconclusive rule).
- Reading: Grid bars are positions 0, 14, 28, ... of each window with close[t+14] inside the window; each coin's mean 14-bar return is the mean over all its grid bars in all windows (not only forecast < 0 ones); the slope's t is from one ordinary least-squares regression on the pooled bars of the coins present in the record (BTC and ETH; BNB is absent); the plan's 'fewer is inconclusive' minimum of 100 is applied as 'not observable' per the workflow rule.
- Size: unusual move +1.40 % per case over 14 bars, 0.088 of the coin's usual move (16.04 %); normal drift in its direction -1.86 %, total -0.46 %; 213 cases
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-04_rsi-below-streak-continuation_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-04_rsi-below-streak-continuation_1d`
Measure: `measure.py`

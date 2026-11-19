---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 240-bar forward return minus coin mean, on forecast (non-overlapping grid, pooled): 0.00279828; OLS slope t: 4.73955 (threshold: confirm: slope t >= 2 and supporting Welch t >= 2; reject: slope t <= -2)
- Supporting check: slope on trending minus slope on unknown grid bars (Welch t): 1.52627, passed: False
- Counts: grid cases with forecast above 0: 821, trending grid cases with forecast above 0: 574, unknown grid cases with forecast above 0: 247, grid cases: 1674
- Decided by: Inconclusive: the main slope has t >= 2 but the supporting difference has t below 2.
- Reading: The raw rsi_above value is read as 50 minus the 336-bar RSI, so the situation is raw < 0 (RSI above 50) on the long side; the main regression uses every grid bar (forecast zero included) and the coin mean is the mean of that coin's grid 240-bar returns over all windows; the regime slopes are OLS slopes whose difference is divided by the root sum of their squared standard errors (Welch t); the plan's minimum counts, when unmet, give 'not observable'.
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h`
Measure: `measure.py`

---
plan: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 72-bar return of top-quintile forecast>0 cases: 0.00682083; ordinary t of the mean: 2.3333 (threshold: confirm: mean > 0 with t >= 2 (and check passes); reject: t <= -2)
- Supporting check: Welch difference top quintile minus other forecast>0 cases (Welch t=2.192): 0.00776953, passed: True
- Counts: top-quintile cases pooled: 1068, top-quintile cases BTCUSD: 199, top-quintile cases ETHUSD: 182, top-quintile cases LTCUSD: 177, top-quintile cases XMRUSD: 184, top-quintile cases XRPUSD: 164, top-quintile cases ZECUSD: 162, other forecast>0 cases: 1766
- Decided by: Mean excess > 0 with t >= 2, and the Welch difference is > 0 with t >= 1 (confirm rule).
- Reading: Top quintile = forecast>0 grid cases (pooled over coins) with forecast >= the pooled 80th percentile (ties at the cutoff included); the coin's mean 72-bar return is the mean over all its non-overlapping grid cases of all windows; the per-coin minimum of 15 applies to every coin in the record; the plan's 'inconclusive' for too few cases is reported as 'not observable'.
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h`
Measure: `measure.py`

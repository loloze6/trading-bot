---
plan: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
idea: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of pooled slope of demeaned 14-bar forward return on forecast (non-overlapping grid, trending, non-zero forecast): 3.31939e-06; OLS slope t: 0.00354393 (threshold: confirm if t >= 2 with timing part > 0; reject if t <= -2; at least 100 independent grid cases)
- Supporting check: timing part of book mean daily return over trending-regime bars: 0.00106233, passed: True
- Counts: independent grid cases: 191, active bars: 2993
- Decided by: The slope's t is between -2 and 2.
- Reading: Low-volatility regime taken from the recorded `regime` == 'trending' (the detector's volrank <= 0.5 rule, not recomputable inside windows without warm-up), side from the raw RSI share against 0.5; coin mean 14-bar return taken over all grid bars of all its windows; a book daily return postRebalance_total_value[t+1]/postRebalance_total_value[t]-1 is attributed to bar t and kept when bar t is trending; fewer than 100 grid cases gives 'not observable'.
- Size: unusual move +1.25 % per case over 14 bars, 0.067 of the coin's usual move (16.04 %); normal drift in its direction -0.00 %, total +1.25 %; 187 cases
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d`
Measure: `measure.py`

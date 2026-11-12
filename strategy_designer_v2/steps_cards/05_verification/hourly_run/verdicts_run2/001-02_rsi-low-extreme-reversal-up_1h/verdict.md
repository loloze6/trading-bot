---
plan: 001-02_rsi-low-extreme-reversal-up_1h
idea: 001-02_rsi-low-extreme-reversal-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: 24-bar forward return, top-decile forecast minus zero-forecast bars (%): -0.127713; Welch t (non-overlapping): -0.439897 (threshold: confirm: positive with t >= 2; reject: negative with t <= -2, or |t| < 2 with >= 150 cases and |estimate| <= 0.1% per 24 bars)
- Supporting check: coins with return per unit avg exposure minus buy-and-hold > 0 (need >= 2): 0, passed: False
- Counts: non-overlapping top-decile cases: 222, non-overlapping neutral cases: 724, coins: 2, coins with positive excess: 0
- Decided by: |t| < 2 but the estimate lies outside the +/-0.1% near-zero bound, which the plan calls inconclusive.
- Reading: The top decile is forecast >= the 90th percentile of all pooled bars' forecasts (and > 0), returns are sampled on the 0,24,48,... grid of each window with Welch t, the supporting check sums per-bar gains and per-bar coin returns over each coin's pooled windows with exposure as mean |allocation|, and with only 2 coins present 'at least 2 of the 3 coins' is applied literally as at least 2 coins.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-02_rsi-low-extreme-reversal-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-02_rsi-low-extreme-reversal-up_1h`
Measure: `measure.py`

---
plan: 001-02_rsi-low-extreme-reversal-up_1h
idea: 001-02_rsi-low-extreme-reversal-up
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: 24-bar forward return, top-decile forecast minus zero-forecast bars: -0.00127713; Welch t (non-overlapping 24-bar grid): -0.439897 (threshold: confirm if positive with t >= 2 (and supporting check holds); reject if negative with t <= -2, or |t| < 2 with >= 150 cases and estimate within +/-0.1% per 24 bars; fewer than 150 non-overlapping top-decile cases is inconclusive)
- Supporting check: coins with return per unit avg exposure minus buy-and-hold > 0 (need >= 2): 0, passed: False
- Counts: non-overlapping top-decile cases: 222, non-overlapping zero-forecast cases: 724, coins: 2
- Decided by: |t| < 2 but the estimate lies outside the +/-0.1% near-zero bound.
- Reading: Top decile is forecast >= the 90th percentile of all pooled bars' forecasts (and > 0), returns are sampled on each window's 0, 24, 48... grid, the per-coin supporting measure sums bar gains over all windows divided by mean |allocation| minus the summed coin returns over the same bars, and 'at least 2 of the 3 coins' is applied literally as at least 2 positive coins among those present.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-02_rsi-low-extreme-reversal-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-02_rsi-low-extreme-reversal-up_1h`
Measure: `measure.py`

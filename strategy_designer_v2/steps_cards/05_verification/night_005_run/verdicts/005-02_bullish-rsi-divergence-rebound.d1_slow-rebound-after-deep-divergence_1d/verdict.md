---
plan: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 20-bar forward return of non-overlapping positive-forecast events: -0.0427527; ordinary t of the mean: -1.55767 (threshold: confirm: mean > 0 with t >= 2 over >= 30 events and Spearman > 0; reject: t <= -2 over >= 30 events)
- Supporting check: Spearman correlation of event forecast vs 20-bar excess return > 0: -0.1089, passed: False
- Counts: non-overlapping events: 54, events BTCUSD: 28, events ETHUSD: 26
- Decided by: Inconclusive rule: t lies between -2 and 2.
- Reading: Situation checked on active bars that have 30 prior closes inside their window (earlier active bars cannot be recomputed and are left out of the agreement share), using the recorded rsi_gap raw value for the RSI gap; the coin's mean 20-bar return is taken on the non-overlapping grid (positions 0, 20, 40, ... of each window) pooled over all its windows; an event at t skips positive bars t+1..t+20 within the same window; the Spearman correlation is between the event's recorded forecast and its excess return.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d`
Measure: `measure.py`

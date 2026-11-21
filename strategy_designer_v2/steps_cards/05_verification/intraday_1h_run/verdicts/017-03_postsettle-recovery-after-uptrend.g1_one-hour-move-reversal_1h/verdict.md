---
plan: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean per-bar excess gain: allocation x (next 1h return - coin's mean hourly return), before costs: 8.14985e-05; t of the mean: 10.2279 (threshold: confirm if t >= 2 and the supporting check passes; reject if t <= -2; else inconclusive)
- Supporting check: Welch t of mean excess gain, bars above minus below the coin's median 720-bar volatility: 1.68905, passed: False
- Counts: bars pooled: 416645, high-volatility group bars: 156480, low-volatility group bars: 156480
- Decided by: The main t is >= 2 but the supporting check's Welch t is below 2 (inconclusive rule).
- Reading: Every bar with a next in-window close counts (flat bars give zero excess), the coin mean is its pooled in-window hourly return, the 720-bar volatility uses the 720 in-window hourly returns up to the bar (sample std), the median is per coin over bars with that volatility, bars exactly at the median are left out of both groups, and the groups are pooled across coins for the Welch t and the 2,000 minimum.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h`
Measure: `measure.py`

---
idea: 002-02_sma-downcross-downward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short average has crossed below the long average -> adapted: "after the cross" becomes "while SMA50 is below SMA200", graded by how far it sits below.
- Comparison: price moves after random points -> kept: compared with the coin's own forward returns over all bars of the same windows.
- Outcome: price keeps falling, more often and further -> kept: forward return of the coin while the short position is held.
- Verdict transfer: yes: the short position grows with the bearish SMA spread, so its forward returns directly test whether price keeps falling after a downward cross.
Forecast: Take the spread between the 50-day and 200-day simple moving averages, (SMA50 − SMA200) / SMA200, the usual daily death-cross pair. Standardise it against its own last 200 values. Clip it at a maximum of 0, so the forecast is short only. It is zero while SMA50 is above SMA200. It turns negative once SMA50 crosses below SMA200, and the short grows as the short average sinks further under the long one, up to −20.
Config: 002-02_sma-downcross-downward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The coin's forward 20-bar return from bars with a negative forecast, minus its mean forward 20-bar return over all bars in the same windows. Each window is cut into non-overlapping 20-bar blocks, so overlapping returns are counted once. The result is a t-statistic across those blocks.
- Supporting check: Within short bars, the slope of forward 20-bar return on forecast size, which should be negative (larger short, larger fall), and the share of short blocks with negative excess return.
- Confirm: Excess forward return while short is negative with t ≤ −2. This means price falls further after downward crosses than after random points. The supporting slope should not have the opposite sign.
- Reject: Excess forward return while short is positive with t ≥ +2. This means price reverses after downward crosses, so the cross marks exhaustion.
- Inconclusive: Any t between −2 and +2 is inconclusive. So is a run with fewer than 6 non-overlapping 20-bar blocks of short exposure (120 short bars across all windows), whatever the t.

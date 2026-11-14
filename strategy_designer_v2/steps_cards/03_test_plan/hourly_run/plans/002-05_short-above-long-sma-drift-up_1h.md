---
idea: 002-05_short-above-long-sma-drift-up
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA above long SMA on hourly bars -> adapted: the on/off "above" zone becomes the graded SMA50-SMA200 spread, clipped at 0, so the position is zero below the cross and grows with the gap above it.
- Comparison: random points -> kept: in-zone forward returns are compared with the coin's unconditional forward returns, which is the buy-and-hold baseline.
- Outcome: price rises over the next bars, more often and further -> kept: forward return and up-share of the coin over the next 24 bars while in the zone.
- Verdict transfer: yes: the test measures drift exactly over the bars where the short average is above the long one, against random bars, in both directions of the verdict.
Forecast: Take the percent spread between the 50-bar and 200-bar simple moving averages of the close. The brief gives no lengths, so these follow the common 50/200 cross convention. Standardise the spread against its own past 200 values, then clip it at 0. The forecast is zero whenever SMA50 is at or below SMA200. It is positive while SMA50 is above SMA200, and it grows with the size of the gap, capped at 20. It is never negative, because the idea only claims an upward drift in the upper zone.
Config: 002-05_short-above-long-sma-drift-up_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The coin's 24-bar forward return from bars with forecast > 0, minus its mean 24-bar forward return over all bars of the same window. This is the excess over holding the coin. It uses non-overlapping 24-bar blocks, pools the six windows and is tested with a t-statistic, before costs.
- Supporting check: The share of in-zone 24-bar blocks with a positive return, minus the same share over all blocks. A one-sided "more often" difference of at least 0 would back the main result.
- Confirm: The pooled excess forward return in the zone is positive with t >= 2, and at least 4 of the 6 windows have a positive excess.
- Reject: The pooled excess forward return in the zone is negative with t <= -2, meaning the drift reverses. A t between -2 and 2 is not a reject.
- Inconclusive: Any t strictly between -2 and +2. Also any confirming t that is not positive in at least 4 of the 6 windows. Also any result with fewer than 150 non-overlapping in-zone 24-bar blocks pooled.

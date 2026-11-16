---
idea: 002-01_sma-cross-up-drift-up
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed above long SMA -> adapted: "after the cross" becomes "while SMA50 is above SMA200", sized by their percent spread.
- Comparison: random points -> kept: compared with the coin's unconditional return over the same bars, as if holding it.
- Outcome: price keeps rising, more often and further -> kept: the coin's forward returns while the position is long.
- Verdict transfer: yes: the test measures whether returns are above buy-and-hold while the short average sits above the long one, the graded form of "after an upward cross".
Forecast: The forecast is the percent spread of SMA(50) over SMA(200) on hourly closes, from `EMASpreadComponent` with `average` "sma". It is standardised against its own last 200 values (target 10, cap 20), then clipped at 0. It is positive and grows with the spread while SMA50 is above SMA200. It is zero while SMA50 is at or below SMA200. It is never short, because the idea concerns upward crosses only. Just after a cross the spread is small, so the position starts small and builds as the trend separates the averages.
Config: 002-01_sma-cross-up-drift-up_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The coin's forward 24-bar log return on bars where the forecast is above 0, minus the mean forward 24-bar log return over all bars of the same window. This is pooled across the 6 windows, before costs. The t-statistic uses only non-overlapping 24-bar blocks, starting each block at a bar with forecast above 0.
- Supporting check: The share of positive forward 24-bar returns when the forecast is above 0, minus the share over all bars. It should have the same sign as the main measure.
- Confirm: The excess return is above 0 with t >= 2, and the supporting check shows a higher hit rate.
- Reject: The excess return is below 0 with t <= -2, meaning moves after upward crosses reverse or lag the coin.
- Inconclusive: Any t between -2 and 2, or a main measure and supporting check that disagree in sign. A verdict needs at least 100 non-overlapping 24-bar blocks with forecast above 0, pooled across the windows.

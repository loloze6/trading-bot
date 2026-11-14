---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed above the long SMA -> adapted: "after the cross" made "while the 50-day SMA is above the 200-day SMA", graded by their percent spread.
- Comparison: random points -> kept: forward returns on bars where the forecast is positive, compared with forward returns on all bars, which is the same as holding the coin.
- Outcome: price keeps rising, more often and further -> kept: the coin's forward return and its share of up moves after those bars.
- Verdict transfer: yes: the graded spread is positive exactly in the post-up-cross state, so a confirm or reject on it transfers to the idea.
Forecast: The forecast is the 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA. It is standardised against its own past 200 values and clipped at 0, so it is long-only. It is zero while the short average is below the long one. It turns positive at the upward cross and grows as the short average pulls further above the long one, up to +20.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The coin's 20-bar forward return on bars where the forecast is above 0, minus its 20-bar forward return on all bars. Use non-overlapping 20-bar blocks, pooled over the 6 windows, before costs.
- Supporting check: The share of positive 20-bar forward returns on forecast-above-0 bars versus all bars, plus the sign of the slope of forward excess return on forecast size.
- Confirm: The excess mean 20-bar forward return is above 0 with t ≥ 2 on non-overlapping blocks, and the up-share and slope are not negative.
- Reject: The excess mean 20-bar forward return has t ≤ -2, meaning moves reverse after up-crosses.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a run with fewer than 10 non-overlapping 20-bar blocks with forecast above 0 across all windows.

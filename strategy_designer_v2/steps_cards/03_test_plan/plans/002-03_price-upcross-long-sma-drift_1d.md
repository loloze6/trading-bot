---
idea: 002-03_price-upcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close crosses above the long average from below -> adapted: "after the cross" made "while above", graded by the percent distance above the SMA200.
- Comparison: random points -> adapted: judged against simply holding BTC over the same bars.
- Outcome: price keeps rising more often and further over the following bars -> kept: forward return measured on the long side.
- Verdict transfer: yes: bars above the SMA200 are the bars that follow up-crosses, so persistence after the cross must show as an edge there, and no edge or a reversal there rejects it.
Forecast: The forecast is the percent distance of the daily close above its 200-day simple moving average. It is standardised over the 200 prior values, so a typical distance gives about 10, capped at 20. It is clipped at 0, so the forecast is zero whenever the close is at or below the SMA200. It is positive and grows the further the close sits above the average. Long only, because the idea concerns up-crosses.
Config: 002-03_price-upcross-long-sma-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The mean 20-bar forward BTC return on bars with forecast > 0, minus the mean 20-bar forward return over all bars. Both are pooled over the 6 windows and taken on non-overlapping 20-bar blocks.
- Supporting check: For each up-cross (forecast goes from 0 to > 0), the share of 20-bar forward returns that are positive, against the unconditional share of positive 20-bar returns.
- Confirm: The in-position minus all-bars difference is above 0 with t ≥ 2 across the non-overlapping blocks, and the share of up-crosses followed by a positive 20-bar return exceeds the unconditional share.
- Reject: The difference is ≤ 0, or the 20-bar forward returns after up-crosses are on average negative (reversal).
- Inconclusive: A positive difference with t < 2, or main measure and supporting check disagreeing. The test needs at least 15 non-overlapping in-position blocks and at least 8 up-crosses; with fewer, it neither confirms nor rejects.

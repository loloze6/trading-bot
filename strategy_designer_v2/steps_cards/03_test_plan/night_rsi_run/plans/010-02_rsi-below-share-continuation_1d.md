---
idea: 010-02_rsi-below-share-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: share of the past 30 days the 14-day RSI spent below 50 -> replaced: the catalogue gives only the current RSI level, not the share of 30 days spent below 50.
- Comparison: a larger share against a smaller share -> kept: a graded forecast that grows with the share.
- Outcome: lower coin return over the next 14 days -> kept: a short position that grows with the share, judged over 14 daily bars.
- Verdict transfer: no: a test on the current RSI level judges a different quantity from the 30-day share of RSI days below 50.
Reason: The share of the last 30 bars on which the 14-bar RSI was below 50 comes from the coin's own closes, and the config could hold it as a graded value. No catalogue component computes it. `RSIPullbackComponent` gives only the current bar's RSI distance from 50. `MovingAverageAgeComponent` counts bars relative to a price average, not RSI. No allowed transform can average or count past values: `standardise` must be the only history op in `transforms`, and `history_transforms` sees one value at a time.

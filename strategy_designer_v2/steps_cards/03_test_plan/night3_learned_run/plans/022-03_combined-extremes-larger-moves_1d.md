---
idea: 022-03_combined-extremes-larger-moves
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a performance-weighted combined score far from its usual value -> replaced: fixed config weights stand in for weights learned from each effect's past predictive record.
- Comparison: equally rare readings of any single signal (momentum, short reversal, nearness to high, volatility) -> kept: each single signal can be recomputed from the coin's prices.
- Outcome: a larger move over the next 5 days, growing as the score moves further out -> kept: 5 bars on daily bars.
- Verdict transfer: no: a fixed-weight blend does not test a combination whose weights follow each effect's recent success.
Reason: The combination weights each effect by how well it predicted returns in the past, relearned over time, using only the coin's own bars. Config weights are fixed constants, and no catalogue component scales a signal by its own trailing predictive record. Weighted means, negative weights and regimes cannot produce a weight that changes with past performance.

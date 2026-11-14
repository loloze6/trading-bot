---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no component places RSI against its own prior peak.
- Comparison: divergent new highs against new highs without divergence -> kept: price at its range top, graded by how far RSI sits below its own range top.
- Outcome: price keeps rising to further highs, long -> kept
- Verdict transfer: no: the situation cannot be measured, so any test result would not transfer to the idea.
Reason: The price side is available: DonchianBreakoutComponent shows where the close sits in its range. Nothing shows where RSI sits relative to its own recent high. RSIPullbackComponent gives only the RSI level, and a percentile of RSI cannot be combined with the required standardise, while in history_transforms it would see a single value. Every composition tried measures RSI's level, not a lower RSI high.

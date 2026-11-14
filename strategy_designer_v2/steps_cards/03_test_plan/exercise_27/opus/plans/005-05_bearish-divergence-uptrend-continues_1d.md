---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no catalogue component compares RSI with its own prior high, so only RSI's level could stand in.
- Comparison: none -> kept
- Outcome: price keeps rising to further highs (long) -> adapted: "after the divergence" made "while the divergence holds", holding period dropped.
- Verdict transfer: no: a proxy built on RSI's level, such as RSI below 50, does not measure a lower RSI high at a new price high, so its verdict would not carry over.
Reason: The situation needs only closes. A graded config could hold it as one forecast that is high when the close sits at the top of its range and RSI sits below the top of its own range over the same window. No catalogue component, alone or combined, compares RSI with its own recent peak: `DonchianBreakoutComponent` gives price's range position, `RSIPullbackComponent` gives only RSI's level, and no op can track a rolling peak of RSI.

---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI makes a lower high -> replaced: no component compares RSI with its own earlier peak.
- Comparison: the RSI peak now against the RSI peak at the previous price high -> replaced: only the RSI level or the price range position is available.
- Outcome: price keeps rising to further highs (long) -> kept
- Verdict transfer: no: the closest build mixes price range position with plain RSI level, which is not a divergence, so its result says nothing about divergence.
Reason: The divergence needs RSI measured against its own recent highs, alongside price measured against its own. No catalogue component does this. `standardise` must be the only history op, so `percentile` cannot rank RSI history, and detector rules read only raw RSI levels. Adding `DonchianBreakoutComponent` to `RSIPullbackComponent` would test "price high while RSI below 50", a different quantity.

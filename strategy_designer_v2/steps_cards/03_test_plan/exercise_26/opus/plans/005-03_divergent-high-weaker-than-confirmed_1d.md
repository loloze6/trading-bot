---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no component places RSI against its own prior high, only RSI's absolute level.
- Comparison: highs with a lower RSI high against highs where RSI also makes a new high -> replaced: the same missing RSI-against-its-prior-high reading is needed.
- Outcome: returns after divergent highs are weaker -> adapted: "after" made "while", with a graded short tilt while the divergence holds.
- Verdict transfer: no: RSI below 50 at a price high is not "RSI below its own prior high", so neither result would carry over to the idea.
Reason: The idea needs RSI's position relative to its own recent peak, which the coin's closes can supply and a graded weighted mean against `DonchianBreakoutComponent` could hold. No catalogue component outputs that position: `RSIPullbackComponent` gives only 50 - RSI, which is a different quantity.

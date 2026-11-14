---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new N-bar high -> adapted: made "while the close is at its 20-bar high", a Donchian regime rule, since "after" becomes "while".
- Comparison: the RSI high is lower than its prior high, against an RSI that also makes a new high -> replaced: no component places RSI against its own recent high, only RSI's level.
- Outcome: weaker (lower) returns after divergent highs than after confirmed highs -> kept: a short, graded by divergence size, is judged against holding over the next bars.
- Verdict transfer: no: a test on the RSI level is not a test of RSI failing to make a new high, so neither result would settle the divergence idea.
Reason: The divergence needs RSI measured against its own maximum over the same window as the price high. That comes from the coin's own closes, and a regime plus a graded component could hold it. But no catalogue component computes it. The one way to build it with transforms, `percentile` on an RSI history, is refused next to `standardise` in strategies (V15), and over a 500-bar lookback it would not match the price window anyway. Pairing `DonchianBreakoutComponent` with `RSIPullbackComponent` only compares price's range position to RSI's level, which is a different quantity.

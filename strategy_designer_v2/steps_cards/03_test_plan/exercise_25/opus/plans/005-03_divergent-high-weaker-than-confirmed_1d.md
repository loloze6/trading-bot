---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high whose RSI high is lower than the prior RSI high -> replaced: the price high can be kept, but no component measures RSI against its own prior high.
- Comparison: new highs where RSI also makes a new high -> replaced: telling the two groups apart needs that same missing RSI-versus-prior-high measure.
- Outcome: weaker returns after divergent highs than after confirmed highs -> adapted: a graded short that grows with the RSI shortfall, judged on gains rising with position size.
- Verdict transfer: no: without RSI's distance from its own prior high, the test cannot separate divergent highs from confirmed ones.
Reason: The new price high can be detected in the coin's own bars, using `DonchianBreakoutComponent` at the top of its range as a regime rule. The divergence itself needs RSI's level relative to its own recent high, and no component computes this. `RSIPullbackComponent` gives only the RSI level. Using `percentile` on its history is refused next to `standardise` (V15), and in the detector it gives only an on/off rule over an unspecified history, not a graded "lower RSI high".

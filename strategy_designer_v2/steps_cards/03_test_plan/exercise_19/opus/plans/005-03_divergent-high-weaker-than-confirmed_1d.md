---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high (close at the top of its recent range) -> adapted: graded closeness to the 14-bar high via `DonchianBreakoutComponent`, gated by a regime rule near the top.
- Comparison: the RSI high is lower than its prior high, against an RSI that also makes a new high -> replaced: no component gives RSI's position within its own recent range, and RSI level is a different quantity.
- Outcome: weaker returns after divergent highs than after confirmed highs -> kept: the forward return of the coin after each case, compared between the two groups.
- Verdict transfer: no: without a measure of RSI against its own prior high, the test cannot separate divergent highs from confirmed highs.
Reason: The divergence needs RSI's position within its own rolling high and low, set beside price's position within its range. RSIPullbackComponent gives only the RSI level, and the percentile op cannot sit next to standardise (V15) or work in history_transforms, so no combination of components computes it.

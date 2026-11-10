---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high whose RSI high is lower than RSI's prior high -> replaced: no component measures RSI against its own recent high.
- Comparison: returns after confirmed new highs (RSI also at a new high) -> kept: a new-high regime with a signed divergence measure would split the two groups.
- Outcome: weaker, reversal-leaning returns after divergent highs -> adapted: graded short exposure within new-high bars, in the regime "while X".
- Verdict transfer: no: without RSI's distance from its own prior high, the divergence itself is not measured.
Reason: The new-high condition can be built as a regime rule on `DonchianBreakoutComponent`'s raw value. No component measures how far the current RSI is below its own highest value over the same lookback. `RSIPullbackComponent` gives only the RSI level. `percentile` on its history cannot sit next to `standardise` in `strategies`, and its window differs from the price window. Using the RSI level instead would test overbought RSI, not divergence, and the brief excludes that question.

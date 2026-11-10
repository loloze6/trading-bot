---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: the close makes a new price high (above its recent highs) -> adapted: graded as where the close sits in its recent range (`DonchianBreakoutComponent`, near +sf at a new high), or as a regime rule on that value reaching its top. "After a new high" becomes "while at or near a new high".
- Comparison: whether the RSI at the new price high is below or above RSI's own earlier high (divergence against confirmation) -> replaced: the catalogue gives only the current RSI level (`RSIPullbackComponent`, 50 - RSI). No component and no allowed transform chain compares RSI with its own rolling maximum. `standardise` must be the only history op, and `percentile` in `history_transforms` sees a single value. Using the RSI level would answer the brief's excluded question (RSI extremes), not divergence.
- Outcome: forward returns after divergent new highs are weaker than after confirmed new highs (a fade, short or less long) -> kept: a forecast that grows short with the size of the divergence at a new high, judged on its forward returns against holding the coin.
- Verdict transfer: no. Without the RSI-against-its-own-high comparison, the test would measure RSI level at new highs, not divergence, so neither a confirm nor a reject would carry over to the idea.
Reason: Everything the idea needs comes from one coin's own closes, and the config's logic could hold it: a regime or graded weight on "price at its range top" times a graded RSI shortfall. No catalogue component measures where the current RSI sits relative to its own recent high, and no composition of the existing components or ops can build that from RSI's history.

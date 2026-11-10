---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: the close makes a new high over its recent window while RSI stays below its own high over the same window (a bearish divergence), as opposed to a new price high where RSI also makes a new high -> replaced: no catalogue component, alone or combined, measures where RSI sits relative to its own recent high. `RSIPullbackComponent` gives only the RSI level, which is a different quantity from "RSI below its prior high".
- Comparison: returns after diverging new highs against returns after confirming new highs -> kept: the forecast would be graded by how far RSI falls short of its high while price is at its high, and the criterion would compare what follows the larger positions with what follows the near-zero ones.
- Outcome: weaker (lower) returns after a diverging new high than after a confirming one -> kept: a short-leaning forecast scaled by the size of the divergence, judged on forward returns against holding the coin.
- Verdict transfer: no: built from the RSI level instead of RSI against its own high, the test would measure "high price with middling RSI", not divergence, so neither a pass nor a fail would settle the idea.
Reason: The divergence needs RSI's position within its own recent range (or its distance below its own rolling high), set against the close's position within its range. The catalogue has the price side (`DonchianBreakoutComponent`) and the RSI level (`RSIPullbackComponent`), but nothing ranks or ranges RSI against its own past. That cannot be built with transforms either: `percentile` cannot sit next to the required `standardise` (rule V15), and a history op in `history_transforms` sees one value. Everything needed is in each coin's own closes, and a graded difference of two range positions fits the config's logic, so only the component is missing.

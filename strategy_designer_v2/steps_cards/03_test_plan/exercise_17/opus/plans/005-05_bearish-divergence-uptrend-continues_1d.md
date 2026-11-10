---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high (close at the top of its recent range) -> kept: `DonchianBreakoutComponent` gives the close's place in its range.
- Comparison: RSI at that bar below its own prior high (a lower RSI high) -> replaced: no component gives RSI against its own recent peak, and absolute RSI level is a different quantity.
- Outcome: price keeps rising to further highs (long) -> kept: a long forecast scored on the forward return against holding the coin.
- Verdict transfer: no: without RSI measured against its own prior high, the test would judge "new high with low RSI", not the divergence.
Reason: The divergence needs RSI compared with its own highest value over the recent window. Every RSI component gives only (50 - RSI). No weighted sum, regime rule or transform keeps a rolling maximum of a component's value over a fixed window, so "a lower RSI high" cannot be built from the catalogue. The data, which is the daily closes, is in the coin's own bars, and a graded per-bar forecast could hold it.

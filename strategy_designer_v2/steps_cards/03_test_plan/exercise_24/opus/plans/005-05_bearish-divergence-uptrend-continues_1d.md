---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> kept: the close's position in its recent range (`DonchianBreakoutComponent`) measures it.
- Comparison: RSI makes a lower high than at the prior price high -> replaced: no component gives RSI's earlier peak, only today's RSI level.
- Outcome: price keeps rising to further highs -> kept: a long forecast, judged by the next bars' return.
- Verdict transfer: no: comparing a price high to a low RSI level is not comparing RSI's current peak to its earlier peak, so neither result would settle the divergence idea.
Reason: The divergence needs RSI's earlier peak, which is in the coin's own closes, and a graded config component could hold it. No catalogue component gives a rolling maximum of RSI, and the only history op allowed in strategies is `standardise`. Weighted sums of `RSIPullbackComponent` and `DonchianBreakoutComponent` can't make "RSI below its earlier high while price is at its high", and a regime gated on the range position still lacks the RSI peak.

---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded as where the close sits in its recent range (`DonchianBreakoutComponent`, near -sf at a new low).
- Comparison: RSI at this low against RSI at the previous price low -> replaced: no component records RSI at a past swing low, only the current RSI level.
- Outcome: price rebounds and recovers part of the decline -> kept: a long position whose gain is the forward return after the low.
- Verdict transfer: no: "RSI not oversold at a range low" is a level reading, not a higher RSI low than at the prior price low.
Reason: The divergence compares RSI at the current price low with RSI at the previous price low, so it needs swing-low detection and the RSI value stored at that earlier pivot. Both come from the coin's own closes, but no component or combination of components computes them; the catalogue has only the current RSI level and the current range position.

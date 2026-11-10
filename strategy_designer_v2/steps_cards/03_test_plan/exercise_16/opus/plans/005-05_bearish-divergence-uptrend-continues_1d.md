---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI makes a lower high -> replaced: no component measures RSI against its own earlier peak, so the lower RSI high cannot be kept.
- Comparison: current RSI peak against RSI at the prior price high -> replaced: no catalogue component or combination gives RSI's prior peak.
- Outcome: price keeps rising to further highs -> kept: a graded long position judged on the forward return.
- Verdict transfer: no: a stand-in such as "price at range top with RSI below 50" is a different situation, so its result would not confirm or reject the divergence idea.
Reason: The divergence needs price at a new high together with RSI below its own earlier peak. Both come from one coin's closes, and the config could hold them as a regime plus a graded component. No catalogue component gives RSI's prior peak or RSI's position in its own range. Combining `DonchianBreakoutComponent` with `RSIPullbackComponent`, in a weighted sum or a score_product, only compares RSI with 50, not with its earlier high.

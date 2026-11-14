---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> adapted: graded as where the close sits in its 14-bar range (DonchianBreakoutComponent), not a strict new-high event.
- Comparison: RSI makes a lower high than at the prior price high -> replaced: no component compares RSI with its own earlier peak.
- Outcome: price keeps rising to further highs -> kept: a long forecast, judged on the following up move.
- Verdict transfer: no: without the RSI lower-high comparison, the test only measures price near its high, which is not the divergence.
Reason: Everything the divergence needs is in the coin's own closes, and a graded component could be combined with the Donchian position or gated in a score_product regime. But no catalogue component measures RSI against its prior high or its recent range. RSIPullbackComponent gives only the level of 50 minus RSI, and no transform takes a rolling maximum of a component's history.

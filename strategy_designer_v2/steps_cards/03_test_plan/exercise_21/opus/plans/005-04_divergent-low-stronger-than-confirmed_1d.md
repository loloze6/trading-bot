---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low over a recent window -> adapted: graded as where the close sits in its 20-bar range (Donchian position).
- Comparison: RSI makes a higher low vs. RSI also making a new low -> replaced: no component places RSI against its own recent low; the RSI level alone would be a different quantity.
- Outcome: returns after divergent lows are stronger (up) than after confirming lows -> kept.
- Verdict transfer: no: the RSI half of the divergence is not computed, so a result could not be attributed to divergence.
Reason: The idea needs RSI's position within its own recent range, read at the same time as price's position within its range. No catalogue component outputs that. Rules and vetoes cannot compare one component with its own past minimum in a graded way, and in `strategies` `standardise` must be the only history op, so `percentile` on RSI is not available there. If that component existed, a weighted combination with the negated Donchian position would express the divergence fully.

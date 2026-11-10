---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI makes a lower high -> adapted: as a graded price-range position minus RSI-range position, but no catalogue component measures RSI against its own prior high.
- Comparison: divergent new highs against new highs where RSI confirms -> adapted: graded, the divergence gap is zero when RSI also sits at its own high.
- Outcome: price keeps rising to further highs -> kept: a long position whose size follows the divergence, judged on forward returns.
- Verdict transfer: no: the situation cannot be built from the catalogue, so no config could confirm or reject the idea.
Reason: The divergence needs RSI's position against its own recent highs, and no component computes it. `RSIPullbackComponent` gives only the RSI level against 50. `DonchianBreakoutComponent` ranks closes only. No combination of components or transforms ranks RSI within its own window. Using the RSI level against 50 instead would replace the "lower high" comparison.

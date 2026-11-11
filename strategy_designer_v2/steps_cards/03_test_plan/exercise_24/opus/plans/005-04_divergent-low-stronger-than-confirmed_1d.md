---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: where the close sits in its recent range (DonchianBreakoutComponent), graded toward the bottom.
- Comparison: new lows where RSI makes a higher low versus new lows where RSI also makes a new low -> replaced: no component measures RSI against its own prior low, so only the RSI level is available.
- Outcome: stronger returns (a bounce up) after higher-RSI-low new lows -> kept: forward returns of the long position against holding the coin.
- Verdict transfer: no: an RSI level is not an RSI higher low, so a result on the level would not confirm or reject the divergence idea.
Reason: The idea needs RSI's current value compared with its own lowest value over the price-low window. The catalogue only gives the RSI level (RSIPullbackComponent). The `percentile` op cannot be used next to `standardise` in strategies, and no combination of components computes a rolling minimum of RSI. All of this is computable from the coin's own closes, so a single new component would close the gap.

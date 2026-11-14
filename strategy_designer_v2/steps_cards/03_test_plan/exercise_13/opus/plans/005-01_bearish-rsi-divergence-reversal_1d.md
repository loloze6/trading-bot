---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new high above its previous swing high -> kept (`DonchianBreakoutComponent` reads where the close sits in its recent range, and it is +sf at a new high)
- Comparison: the RSI at the new high against the RSI at the previous price high, where a lower RSI means a bearish divergence -> replaced: no component records the RSI value at the bar of the previous price high. The only RSI reading available is `RSIPullbackComponent`, which is the current RSI against the fixed level 50. That is a different quantity from RSI against its own value at the prior high.
- Outcome: price falls and gives back part of the run-up to the high -> adapted: a graded short whose size follows the size of the divergence, held while the divergence is present instead of for a fixed retracement period
- Verdict transfer: no: a config built from "price near its range top while RSI is below 50" tests whether RSI weakness at a high matters, not whether RSI makes a lower high than at the previous price high. Its result would neither confirm nor reject the divergence idea.
Reason: The divergence needs the RSI value on the bar of the previous price swing high, to compare with the RSI at the current new high. No catalogue component records a past pivot's RSI, and no transform or composition can fetch a value from a specific earlier bar chosen by price. All the data is in the coin's own closes, and a graded component could carry it, but the indicator does not exist.

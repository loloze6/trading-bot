---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new high (the highest close of its recent window) -> adapted: the threshold "new high" becomes a regime rule on `DonchianBreakoutComponent` (period 20, the usual 20-day high; raw value `gte` 20 means the close is the highest close of the window). The condition is the idea itself, so a regime fits it.
- Comparison: RSI at this new price high is lower than RSI was at the earlier price high (a lower RSI high) -> replaced: no component or combination in the catalogue measures RSI against its own earlier peak. `RSIPullbackComponent` gives only the RSI level against 50. `standardise` divides by a past mean and does not subtract a past maximum. The rule and veto operators compare a value with a fixed constant, not with an earlier value of RSI.
- Outcome: price keeps rising to further highs over the following bars (long, continuation) -> kept: a long position that is larger when the divergence is larger, judged on later returns against holding the coin.
- Verdict transfer: no: standing in for "RSI below its earlier high" with "RSI below 50" or with plain RSI weakness tests a different quantity, so neither a confirmation nor a rejection would carry over to the divergence idea.
Reason: Every input to the divergence comes from one coin's closes, and the config could hold it: a regime for "close at a new high" plus a graded long component for "how far RSI sits below its earlier high". But no catalogue component computes RSI relative to its own recent peak, and no composition of the existing components or ops (weights, negate, standardise, clip, regime rules against constants) can produce a rolling maximum of RSI.

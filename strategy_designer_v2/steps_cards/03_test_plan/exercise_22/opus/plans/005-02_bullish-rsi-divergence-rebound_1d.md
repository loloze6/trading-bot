---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low below its previous low -> kept
- Comparison: RSI at the new low is higher than RSI at the previous price low -> replaced: no component finds the earlier swing low or reads RSI at it
- Outcome: price rebounds and recovers part of the decline into the low -> adapted: a graded long forecast while the divergence is present, judged on the forward return
- Verdict transfer: no: without the comparison of RSI at the two lows, a test would measure new lows or RSI level, not divergence
Reason: The divergence needs the previous swing low of the close and the RSI value at that bar, compared with the RSI at the current new low. No catalogue component computes this. Weighted sums of `DonchianBreakoutComponent` and `RSIPullbackComponent` only add "price near its low" to "RSI level". They never compare the RSI at two price lows, and the regime modes cannot do it either.

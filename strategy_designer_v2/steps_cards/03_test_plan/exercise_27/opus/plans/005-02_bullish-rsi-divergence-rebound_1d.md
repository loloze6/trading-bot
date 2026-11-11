---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low below its previous price low -> adapted: graded closeness of the close to its recent range low (Donchian position, negated).
- Comparison: RSI makes a higher low than at the previous price low -> replaced: no component reads RSI at a past price low, only RSI's current level against 50.
- Outcome: price then rebounds and recovers part of the decline -> adapted: holding period dropped, long only while the situation lasts.
- Verdict transfer: no: RSI's level against 50 is a different quantity from RSI now against RSI at the prior low, so a result would not judge the divergence.
Reason: The idea compares RSI at the current price low with RSI at the previous price low. That needs swing lows found in the coin's own closes and the RSI value stored at each one. The catalogue has RSI only as its current level, and no component finds swing lows, so no combination can measure that comparison. All the data is in one coin's closes, and a per-bar number could hold it.

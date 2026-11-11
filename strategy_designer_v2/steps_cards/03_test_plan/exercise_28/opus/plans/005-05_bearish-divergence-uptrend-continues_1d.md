---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no component compares RSI with its own earlier peak; only RSI against 50 is available.
- Comparison: the current RSI high against the RSI high at the earlier price high -> replaced: RSI's prior peak is not computed by any component, alone or combined.
- Outcome: price keeps rising to further highs -> adapted: graded long held while the divergence lasts, judged on forward returns.
- Verdict transfer: no: RSI against 50 at a price high is not a divergence, so neither result would settle the idea.
Reason: The divergence needs RSI compared with its own earlier peak, while price sits at its range high. That can be computed from the coin's own closes, and a graded forecast could hold it. No catalogue component gives RSI's rolling maximum or its position in its own range. Weighted sums of `DonchianBreakoutComponent` and `RSIPullbackComponent` only give RSI's level against 50, which is a replacement.

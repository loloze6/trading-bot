---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component records RSI at the prior price low.
- Comparison: against new price lows where RSI also makes a new low -> replaced: no component separates confirmed lows from divergent lows.
- Outcome: returns after divergent lows are stronger (upward) -> kept: the forward return after the position, against holding the coin.
- Verdict transfer: no: no catalogue combination measures RSI at the earlier low, so any result would test a different signal.
Reason: The idea needs RSI on the current new low compared with RSI on the previous price low, so earlier swing lows must be remembered. All of this comes from one coin's closes, and a graded component could carry it. No catalogue component computes it, and neither combinations nor history ops can, because the only history op allowed in `strategies` is `standardise` and regime rules compare raw values only.

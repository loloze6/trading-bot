---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a new price high reached with a lower RSI high -> replaced: no component measures RSI against its own prior high.
- Comparison: returns after confirmed new highs, where RSI also makes a new high -> replaced: the same missing measure is needed to separate confirmed highs from divergent ones.
- Outcome: weaker returns after divergent highs than after confirmed highs -> kept: a graded forecast that is short on divergence and long on confirmation, measured on forward returns.
- Verdict transfer: no: substitutes such as the RSI level or the price's range position do not measure divergence, so neither result would speak to the idea.
Reason: Divergence needs RSI's current value compared with its own recent high, taken at bars where the close is at its recent high. The catalogue has RSI only as a level (`RSIPullbackComponent`) and range position only for price (`DonchianBreakoutComponent`). `standardise` must be the only history op, so a rolling-max or percentile of RSI cannot be built from transforms, and combining the two components gives "high price, low RSI level", not a lower RSI high.

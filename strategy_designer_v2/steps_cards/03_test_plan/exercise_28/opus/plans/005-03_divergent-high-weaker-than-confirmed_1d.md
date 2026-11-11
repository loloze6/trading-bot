---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a new price high with a lower RSI high than at the prior high -> replaced: no catalogue component measures RSI against its own prior high.
- Comparison: returns after divergent new highs versus returns after new highs where RSI also makes a new high -> kept: the graded divergence size would separate the two cases.
- Outcome: returns after divergent highs are weaker, a reversal down -> adapted: "after X" made "while X", a graded short that grows with the divergence.
- Verdict transfer: no: RSI level is not RSI relative to its prior high, so a test on RSI level would not transfer to the idea.
Reason: The price side of the idea can be built from the coin's own closes: `DonchianBreakoutComponent` gives the close's position in its range. The divergence also needs RSI's position against its own recent highs, and no component computes it. `RSIPullbackComponent` gives only the RSI level, which neither weighting nor sign flips can turn into "RSI below its prior high". The graded forecast would be the price range position minus the RSI range position, short when price is at its high and RSI is not.

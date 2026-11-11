---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high whose RSI high is lower than RSI's prior high -> replaced: no component measures RSI against its own prior high.
- Comparison: returns after divergent new highs against returns after new highs where RSI also makes a new high -> adapted: a graded difference between price range position and RSI range position.
- Outcome: returns after divergent highs are weaker, a reversal down -> adapted: a graded short that grows with the divergence, held while it lasts.
- Verdict transfer: no: without RSI's own new-high reading, the test cannot tell a divergent high from a confirming one.
Reason: The idea needs RSI compared with its own recent high, read on the same bar as price's position in its range. The bars hold everything this needs, and the config could combine it with `DonchianBreakoutComponent` by weights. But the catalogue gives RSI only as a level (`RSIPullbackComponent`, 50 - RSI). No component, alone or combined, gives RSI's place in its own recent range, so "RSI also makes a new high" cannot be measured.

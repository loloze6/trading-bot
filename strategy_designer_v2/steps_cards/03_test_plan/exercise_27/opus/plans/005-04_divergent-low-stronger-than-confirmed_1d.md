---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded as the close's position near the bottom of its recent range (`DonchianBreakoutComponent`).
- Comparison: RSI makes a higher low versus RSI also making a new low -> replaced: no component measures RSI against its own prior low.
- Outcome: returns after divergent new lows are stronger (more upward) than after confirmed new lows -> kept: forward returns of long positions, compared between the two kinds of low.
- Verdict transfer: no: without RSI's position against its own recent low, a test cannot tell divergent new lows from confirmed ones.
Reason: The idea compares RSI's current low with its earlier low over the same window in which price makes its new low. The catalogue gives RSI's level (`RSIPullbackComponent`) and price's range position (`DonchianBreakoutComponent`), but nothing that places RSI within its own recent range. `percentile` cannot stand in for this, because `standardise` must be the only history op in a strategies pipeline. No combination of the existing components gives the graded divergence, price's range position minus RSI's range position.

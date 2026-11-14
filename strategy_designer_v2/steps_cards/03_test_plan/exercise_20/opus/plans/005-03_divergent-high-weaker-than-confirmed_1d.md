---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: new price high while the RSI high is lower -> replaced: no catalogue component measures RSI against its own recent high.
- Comparison: divergent new highs against confirmed new highs (RSI also at a new high) -> adapted: graded as the gap between the close's range position and RSI's range position.
- Outcome: weaker returns after divergent highs than after confirmed ones -> kept.
- Verdict transfer: no: the only catalogue proxy is the RSI level, not RSI against its prior high, so the test would measure a different situation.
Reason: The divergence needs RSI compared with its own recent maximum, which can be computed from the closes alone. The catalogue gives only the RSI level (`RSIPullbackComponent`). No transform or composition turns that level into "RSI below its recent high". `DonchianBreakoutComponent` measures this only for the close, not for RSI.

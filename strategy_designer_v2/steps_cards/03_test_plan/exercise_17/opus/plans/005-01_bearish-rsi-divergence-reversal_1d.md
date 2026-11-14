---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> adapted: graded as where the close sits in its recent range (DonchianBreakoutComponent), not a new-high event.
- Comparison: RSI's peak is below its level at the previous price high -> replaced: no component finds the earlier price high or reads RSI there, only the current RSI level.
- Outcome: price falls back and gives up part of the run-up -> kept: a short position whose gains are measured over the following bars.
- Verdict transfer: no: without RSI at the earlier high, a test would measure "high in range with RSI not extreme", not a divergence.
Reason: Only the coin's own closes are needed, and a graded per-bar divergence value fits the config. No catalogue component compares RSI at the current price high with RSI at the previous one. Combining DonchianBreakoutComponent with RSIPullbackComponent only gives the current RSI level, not the drop in RSI between the two highs.

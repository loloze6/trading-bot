---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> adapted: graded as where the close sits in its 14-bar range (DonchianBreakoutComponent), +sf at the top.
- Comparison: RSI's high now is lower than RSI at the previous price high -> replaced: no component reads RSI at earlier price highs, so only the current RSI level could stand in.
- Outcome: price falls back from the high -> kept: a short whose size grows with the divergence, judged on the next bars' returns.
- Verdict transfer: no: a low RSI at a high close is not RSI making a lower high than at the previous price high, so neither result would transfer.
Reason: The divergence compares RSI at the current price high with RSI at the previous price high. That needs RSI's own recent extremes, which no catalogue component computes. Combining DonchianBreakoutComponent with RSIPullbackComponent only compares price position with the current RSI level, not with RSI at the earlier high. The data is all in the coin's closes, and a graded component could hold the comparison.

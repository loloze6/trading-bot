---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high, as in `DonchianBreakoutComponent` near +sf -> kept
- Comparison: RSI at this high is lower than RSI at the previous price high -> replaced: no component reads RSI at a past swing high.
- Outcome: price falls back and retraces part of the run-up -> adapted: graded short while the divergence lasts, holding period dropped.
- Verdict transfer: no: without the RSI comparison, the test only measures new highs, not divergences.
Reason: The catalogue can say where the close sits in its range, and it can give RSI against 50. It has no component that compares the current RSI with the RSI at the previous price high. Combining those components only measures "new high while RSI is below 50", which is a different quantity.

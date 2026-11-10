---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> adapted: a regime rule fires on bars where the close is the highest close of its recent window (`DonchianBreakoutComponent` raw value at +sf).
- Comparison: RSI at this high is below RSI at the previous price high -> replaced: no catalogue component reads RSI at the previous swing high, and RSI level or price-range position are different quantities.
- Outcome: price falls back and retraces part of the run-up -> adapted: a graded short held while the divergence lasts, with the holding period dropped.
- Verdict transfer: no: without the RSI-at-previous-high comparison, the test would judge new highs with low RSI, not divergence.
Reason: The divergence needs RSI at the current high compared with RSI at the previous price high, all computable from the coin's own closes and placeable as a graded component inside a "new high" regime. No catalogue component, alone or combined, reads RSI's value at a prior swing high or RSI's position against its own recent peak.

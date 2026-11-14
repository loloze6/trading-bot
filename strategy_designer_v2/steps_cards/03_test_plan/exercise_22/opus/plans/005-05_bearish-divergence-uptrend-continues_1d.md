---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no catalogue component compares RSI with its level at the prior price high.
- Comparison: none in the idea (the brief compares with new highs without divergence) -> kept
- Outcome: price keeps rising to further highs (long) -> kept
- Verdict transfer: no: a stand-in for "RSI lower high" would test a different situation, so neither a confirm nor a reject would carry over to the idea.
Reason: Donchian range position can show the new price high, and RSIPullback can give the RSI level. But no component, and no combination the guide allows, measures RSI's shortfall below its own recent peak. `standardise` must be the only history op in a strategies component, and the detector's percentile ranks RSI against its whole history, not against its value at the prior swing high.

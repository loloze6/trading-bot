---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> adapted: graded as where the close sits in its recent range (DonchianBreakoutComponent).
- Comparison: RSI makes a lower high than at its prior price high -> replaced: no catalogue component compares RSI with its own earlier peak.
- Outcome: price keeps rising to further highs -> kept: a long position while the divergence lasts, judged on the next returns.
- Verdict transfer: no: RSI level (RSIPullbackComponent) is not RSI below its own prior high, so a result would not speak to divergence.
Reason: The divergence needs RSI measured against its own recent peak, while the close sits at its recent peak. That is computable from one coin's closes and could be held as a graded difference. But no component tracks a rolling maximum or range position of RSI, and `standardise` must be the only history op, so `percentile` cannot be run over RSI history either.

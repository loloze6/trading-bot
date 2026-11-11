---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> kept: the Donchian close position at the top of its range measures it.
- Comparison: RSI makes a lower high than at the prior price high -> replaced: no component measures RSI against its own earlier peak.
- Outcome: price keeps rising to further highs -> kept: a long position profits if price rises next.
- Verdict transfer: no: without RSI measured against its own prior peak, the test would not measure a divergence.
Reason: The comparison needs the current RSI measured against its own recent peak, at the moment the close sits at a new high. The RSI components give only the RSI level (50 - RSI). Mixing that level with Donchian position, or ranking it with percentile in a score-mode detector, measures RSI against its long-run distribution rather than against its earlier high. A weighted mean is also additive, not the "and" the divergence needs.

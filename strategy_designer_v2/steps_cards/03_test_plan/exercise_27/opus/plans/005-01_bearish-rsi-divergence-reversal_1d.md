---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no catalogue component reads RSI at swing highs, so only a proxy could stand in.
- Comparison: RSI at this high against RSI at the previous price high -> replaced: no component keeps RSI's value at the prior price peak.
- Outcome: price falls back, retracing part of the run-up -> kept: a short position gains when the close falls over the next bars.
- Verdict transfer: no: any buildable proxy, such as range position minus RSI level, measures something other than the divergence, so a result would not transfer.
Reason: The divergence needs the close and RSI only, and a graded per-bar value fits the config's logic. But no component compares RSI at the current price high with RSI at the previous price high. Donchian, RSIPullback and the transforms cannot recall RSI's value at the prior high.

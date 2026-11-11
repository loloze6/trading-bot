---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no component finds price swing highs, so only RSI level at the top of the Donchian range is available.
- Comparison: RSI now vs RSI at the previous price high -> replaced: RSI against a fixed 50, not against its value at the prior peak.
- Outcome: price falls back, retracing part of the run-up -> adapted: graded short forecast held while the divergence lasts, no fixed holding period.
- Verdict transfer: no: a test of "RSI weak near the range top" is not a test of a lower RSI peak than at the previous price high.
Reason: The idea needs RSI at the current new high compared with RSI at the bar of the previous price high. That requires finding swing highs and remembering RSI at them, and no catalogue component or composition does this. The data is in the coin's own closes, and a graded per-bar value fits the config's logic, so only the component is missing.

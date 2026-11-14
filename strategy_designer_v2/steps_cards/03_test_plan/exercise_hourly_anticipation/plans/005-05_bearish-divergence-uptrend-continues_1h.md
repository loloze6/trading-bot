---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI makes a lower high -> replaced: no component compares RSI with its value at the prior price high.
- Comparison: current RSI against RSI at the previous price high -> replaced: RSIPullback only measures RSI against 50, and Donchian only measures price within its own range.
- Outcome: price keeps rising to further highs -> kept: a long forecast scored on the next bars' returns.
- Verdict transfer: no: a test built from RSI-versus-50 and price-in-range would measure "high price with soft RSI", not a lower RSI high at a new price high.
Reason: The divergence needs RSI at the current price high compared with RSI at the prior swing high. Everything it needs comes from one coin's closes, and a per-bar graded value fits the config's logic. No catalogue component, alone or combined, computes RSI against its own earlier peak. Donchian plus RSIPullback weighted, or percentile of RSI history in a score regime, only ranks RSI against 50 or a long window, not against the prior high.

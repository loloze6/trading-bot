---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high -> adapted: graded position of the close in its recent range (DonchianBreakoutComponent).
- Comparison: RSI now below the RSI at the previous price high -> replaced: no component or combination reads RSI at the prior swing high, only the current RSI level.
- Outcome: price falls back from the high, so the trade is short -> kept: a negative forecast gains when price falls.
- Verdict transfer: no: without RSI at the previous high, a test cannot tell divergent new highs from plain new highs, and the brief's rejection rule depends on that contrast.
Reason: The divergence needs the RSI value at the previous price high, compared with the RSI at the current new high. That memory of swing points can be computed from the coin's own closes, but no catalogue component computes it. RSIPullback, Donchian, percentile or a weighted mean only compare current levels. Percentile on RSI cannot follow standardise, and it would rank RSI against its whole window, not against the prior price high.

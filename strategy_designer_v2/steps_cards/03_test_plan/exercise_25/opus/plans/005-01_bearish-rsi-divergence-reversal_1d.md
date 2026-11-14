---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no component records the RSI at a past price high, so only a proxy (range position against RSI level) could be built.
- Comparison: current RSI against the RSI at the previous price high -> replaced: no component, alone or combined, gives the RSI at the prior swing high.
- Outcome: price then falls and retraces part of the run-up -> adapted: graded short while the divergence holds, with the holding period dropped.
- Verdict transfer: no: a proxy such as "close high in its range while RSI is moderate" is not a divergence, so its result would not judge the idea.
Reason: The idea needs the RSI at the previous price high, compared with the RSI at the current new high. The data is all in the coin's own closes, but no catalogue component keeps a past swing high's RSI or RSI's rolling maximum. Compositions such as Donchian position minus standardised RSIPullback measure RSI level, not a lower RSI high, and would be a replacement.

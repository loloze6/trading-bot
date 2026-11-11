---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded closeness of the close to the bottom of its recent range (Donchian position).
- Comparison: RSI makes a higher low than at the prior price low -> replaced: no component places RSI against its own prior low.
- Outcome: price keeps falling to further lows -> adapted: a short position gains while the divergence holds ("after" made "while").
- Verdict transfer: no: using RSI's level instead of its higher low would test an RSI-extreme idea, which the brief explicitly excludes.
Reason: The divergence needs RSI compared with its own recent low, but the catalogue has only the RSI level. The single allowed history op, `standardise`, cannot rank RSI within its own range, and no combination of components gives the RSI's prior low. Everything needed is in each coin's own closes, and a graded product of "price near its range low" and "RSI above its range low" would fit the config's logic once that component exists.

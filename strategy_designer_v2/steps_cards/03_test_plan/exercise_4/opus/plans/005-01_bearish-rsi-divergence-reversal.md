---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI now with RSI at the previous price high, a lower high in RSI against the last peak. No catalogue component or transform can give a lagged or peak-tracked RSI value: rules see only the latest raw value, and `standardise` must be the only history op. Any composition, such as "price near the top of its Donchian range while RSI is lowish", measures how slowly the climb went, not a divergence from the prior peak. So it cannot separate divergent new highs from non-divergent ones, which is the comparison the brief's falsification needs.

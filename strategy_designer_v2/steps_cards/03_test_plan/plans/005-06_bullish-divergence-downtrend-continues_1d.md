---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea needs RSI's value now compared with its value at the earlier price low, so we can tell whether RSI made a higher low. The config has no memory of past turning points, and the catalogue has no component that tracks RSI's range or past lows. Without that comparison the divergence cannot be built; a config that kept only "price at a new low" would drop the very condition the idea is about.

---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at the new price high with RSI at the previous price high. That needs the config to remember where the earlier swing high was and what RSI read there, and the config has no memory of past turning points. Every catalogue component reads only its current window, so the "lower high in RSI than at the previous high" comparison, which is the idea itself, cannot be built. A proxy such as "close near the top of its range while RSI is low" would drop that comparison.

---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Untestable: The idea compares RSI at the new price high with RSI at the previous price high, and the config has no memory of past turning points, so it cannot find the earlier high or read RSI's value there. No catalogue component gives RSI's position within its own recent range, so even a proxy such as "close at the top of its range while RSI is not" cannot be built without dropping the lower-high comparison the idea is about.

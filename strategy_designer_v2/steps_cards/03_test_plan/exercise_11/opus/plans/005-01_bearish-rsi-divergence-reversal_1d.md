---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at the current price high with RSI at the previous price high, and the config keeps no memory of past turning points, so it cannot recall the RSI value at the earlier high. A proxy such as "price near the top of its range while RSI is below its own average" would drop the high-to-high comparison that defines the divergence.

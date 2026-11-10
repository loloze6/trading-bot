---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at today's new price low with RSI at the previous price low. The config has no memory of past turning points, so it cannot recall the earlier low or the RSI value there. No catalogue component measures price-RSI divergence, and approximations such as "close at the bottom of its range while RSI is not oversold" would drop the higher-low comparison the idea is about.

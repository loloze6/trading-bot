---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Untestable: The idea requires comparing RSI at the current price low with RSI at the previous price low, and the config cannot remember past turning points. No catalogue component tracks the RSI value at an earlier swing low, and none measures where RSI sits within its own recent range. A proxy, such as price near the bottom of its range while RSI is not oversold, would drop the higher-low comparison that defines the divergence.

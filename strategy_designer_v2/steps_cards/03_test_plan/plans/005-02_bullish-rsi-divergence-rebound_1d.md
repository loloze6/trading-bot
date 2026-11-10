---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at the new price low with RSI at the previous price low. The config keeps no memory of past turning points, and no catalogue component gives RSI's value at an earlier low or its rolling minimum. Without that comparison the config could only test "price near its range low while RSI is not oversold", which drops the divergence the idea is about.

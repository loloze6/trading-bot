---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at the current price low with RSI at the previous price low. That needs swing lows to be found and RSI remembered at the earlier one. No catalogue component or transform can find pivots or store an indicator's value at a past event; the only state components keep is their own history. A blend of range position (Donchian) and the RSI level drops that comparison, so it would test "price low in its range while RSI is not low", not a higher RSI low at a new price low.

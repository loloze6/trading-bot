---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea depends on comparing two lows: price setting a new low while RSI sits above the RSI reading at the earlier price low. The catalogue has no way to locate the earlier low or recall an RSI value from the past. There is no rolling minimum of RSI, no lagged RSI, and `percentile` cannot run on the RSI history because `standardise` must be the only history op. Any composition, such as the Donchian range position minus the RSI level, compares where price sits in its range with the RSI level now, not with RSI's earlier low. It drops the comparison the idea rests on.

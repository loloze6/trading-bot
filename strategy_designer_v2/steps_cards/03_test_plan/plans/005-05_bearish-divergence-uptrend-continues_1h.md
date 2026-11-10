---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Untestable: The idea depends on comparing RSI at the new price high with RSI at the previous price high, and checking that it is lower. The catalogue has no lagged RSI, no rolling maximum of RSI, and no way to rank RSI against its own past inside a graded forecast, because `standardise` must be the only history op. Any config would therefore drop that comparison and test plain "price near its range high" or "RSI level" instead, which is not a divergence.

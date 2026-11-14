---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at the current price high with RSI at the previous price high. The catalogue has no swing-high detection and no way to read RSI's past peak: `RSIPullbackComponent` gives only the current RSI level, and a percentile of RSI against its own history would need a second history op beside `standardise`, which V15 refuses. Any graded stand-in, such as the Donchian range position minus the RSI level, would drop that two-peak comparison, so it would not test the idea.

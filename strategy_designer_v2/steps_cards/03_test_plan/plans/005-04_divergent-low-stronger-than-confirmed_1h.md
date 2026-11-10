---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Untestable: The idea compares the RSI low at a new price low with the RSI low at the previous price low, and nothing in the catalogue can recall that earlier reading: there is no rolling minimum of RSI, no RSI value at the bar of the prior low, and `standardise` compares only against the mean absolute size of past values. A config could gate on "close near its 48-bar low" (Donchian) and size by the current RSI level, but that drops the higher-low versus lower-low comparison, which is the divergence the idea is about.

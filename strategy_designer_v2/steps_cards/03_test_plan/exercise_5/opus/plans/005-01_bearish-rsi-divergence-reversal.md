---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea needs RSI at the previous price high, compared with RSI at the current new high. No catalogue component finds swing highs or stores an indicator's value at an earlier peak, and `standardise` only compares against the average of past values, not the last peak. The nearest proxies do not measure divergence. A "price at the top of its range" regime with a graded RSI component can only size by RSI's absolute level, and an offset to centre it would put a constant inside a regime, which is not allowed. An ungated "range position minus RSI" spread measures range versus short-term momentum on every bar, which is a different idea.

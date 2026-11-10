---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Untestable: The idea compares RSI at the current price low with RSI at the previous price low. That needs swing lows to be found and the RSI value at an earlier low to be remembered. No catalogue component, transform or regime rule can do either: rules read only the latest raw value, there are no lagged or extremum-anchored indicators, and `standardise` only rescales. A config would therefore drop the higher-low comparison that defines the divergence, leaving only "price at a low in its range" or "RSI level", which is a different idea.

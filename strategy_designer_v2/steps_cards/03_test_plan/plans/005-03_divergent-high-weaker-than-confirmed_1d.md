---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares the RSI at a new price high with the RSI at the earlier high, and the catalogue has no component that gives RSI's own recent maximum or rank. The only route to an RSI rank is a `percentile` history op, which cannot sit next to the required `standardise` step. A config could only use the RSI level at new highs, which drops the lower-RSI-high comparison the idea is about.

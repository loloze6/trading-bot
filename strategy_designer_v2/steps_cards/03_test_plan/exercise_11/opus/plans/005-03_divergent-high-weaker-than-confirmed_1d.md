---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares the RSI high at today's new price high with the RSI high at the previous price high, so it needs the RSI value at an earlier turning point. The config keeps no memory of past turning points and has no component for an RSI rolling high or RSI range position. The closest substitute would rank RSI against its own history with `percentile`, but that cannot be combined with `standardise`, which must be the only history op. Dropping that comparison would remove the divergence the idea is about.

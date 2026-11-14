---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares the RSI at today's new price low with the RSI at the previous price low (a higher RSI low against a lower one), and the config keeps no memory of past turning points, so it cannot know the RSI value at the earlier low. The catalogue also has no RSI-range or RSI-low component. A weighted sum of where the close sits in its range and the RSI level would drop that low-to-low comparison, which is what the idea is about.

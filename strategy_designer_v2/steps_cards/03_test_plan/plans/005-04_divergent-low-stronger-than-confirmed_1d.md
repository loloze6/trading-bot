---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI now with RSI at the earlier price low (a higher RSI low versus a new RSI low), and the config has no memory of past turning points. The catalogue also has no component that gives RSI's position within its own recent range, so the config can see that price is at a new low but not whether RSI made a new low too, and dropping that comparison would drop the idea.

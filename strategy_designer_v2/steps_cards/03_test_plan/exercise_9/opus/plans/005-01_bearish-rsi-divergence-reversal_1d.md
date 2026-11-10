---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at the new price high with RSI at the previous price high. The catalogue has no way to find that earlier high or read the RSI value there: there is no swing-high detection, no rolling maximum of RSI, and no lagged value of a component. Any config could only use today's RSI level at a high in the price range. That drops the peak-to-peak comparison that defines a divergence and turns the test into the RSI-level question the brief excludes.

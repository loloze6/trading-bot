---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: On each of BTC, ETH and BNB, before costs, the mean next-bar coin return on bars where the forecast is in its top decile (the highest RSI readings) is above the mean next-bar return on bars where the forecast is below 2 (RSI near or below 50). The strategy's gross return must also beat buy-and-hold scaled to the strategy's average allocation.
Reject: On all three coins, the top-decile forecast bars are followed by next-bar returns equal to or below those after neutral bars, which would mean no effect or reversal. The strategy's gross return must also fail to beat exposure-matched buy-and-hold.
Deviation: "After RSI reaches a high extreme" becomes "while RSI(14) is above 50, a long position that grows with the square of how far RSI sits above 50, relative to its last 60 bars". The test holds the position bar by bar and lets it fade as RSI falls back, rather than measuring a fixed horizon after a threshold event. Low-RSI extremes are left out: the forecast is flat below RSI 50.

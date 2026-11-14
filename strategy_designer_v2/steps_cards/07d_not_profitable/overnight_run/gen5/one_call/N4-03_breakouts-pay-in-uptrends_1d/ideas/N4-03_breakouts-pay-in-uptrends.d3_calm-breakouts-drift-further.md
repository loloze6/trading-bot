---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-03_breakouts-pay-in-uptrends
line: 7.d not profitable
backtest: N4-03_breakouts-pay-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A close near its 20-day high in an uptrend is followed by a larger 10-day rise when the coin's recent 20-day volatility is low than when it is high.
Consequence: Weight breakout longs toward calm conditions and size them down when daily volatility is elevated.
Why:
- F7: Long gains shrink as volatility rises. Long bars gross +0.00153 a day in the calm third of 20-day volatility, +0.00118 in the middle third and +0.00062 in the volatile third. Shorts lose most in the volatile third (−0.00111).
- F2: Long trades pay only when the 60-day trend is up. In the trending regime, forecast-active bars beat holding over 10 days by +0.0276 when the past 60-day return is positive (t 2.19, 253 cases), and by −0.0029 when it is negative (t −0.25, 288 cases).

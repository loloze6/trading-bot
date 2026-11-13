---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A one-day drop in a coin whose own 60-day return has fallen to zero or below is followed by a below-average next-day return. The drop marks continuation of a fading trend rather than a dip to buy.
Consequence: A trader stops buying dips once the coin's 60-day return is no longer positive, cutting the losing holdings inside the deep falls.
Why:
- F1: The Calmar failure comes from one stretch of windows: book drawdown measured on daily book returns reaches -36.2% across w11–w17, against a 21.1% annualised mean, with within-window falls of -18.5% (w11), -19.1% (w13) and -21.3% (w17); w1–w10 never fall below -11.0%.
- F5: Held bars whose own 60-day return, computed from the bars, is ≤0 have a next-day excess of -0.0049 (t -1.98, n 282). Held bars in 2018 have -0.0150 (t -2.10, n 126). Dips bought once the uptrend has faded are followed by underperformance.
- F6: The windows holding the drawdowns (w11–w17, w20–w23) give a held-bar excess of only +0.0012 (t 0.83, n 1403) with summed losses of -20.9. The other windows give +0.0032 (t 2.80, n 1367) with losses of -9.0.

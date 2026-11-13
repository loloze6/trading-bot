---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.g patterns
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Outside a 20- and 60-day uptrend, when a coin closes a large up day while its 20-day volatility is high for that coin, the next day returns less than the coin's average.
Consequence: A trader could refuse longs, or fade, after high-volatility up spikes in coins that are not in an uptrend.
Why:
- F4: Outside the uptrend, a large up day (z > 1) in the coin's top volatility third was followed by a next-day excess return of -0.87% (t -4.03, n 569, hit 39.9%); in the lower two volatility thirds the same up day gave about -0.1% to 0 (t -0.68 and -0.15).

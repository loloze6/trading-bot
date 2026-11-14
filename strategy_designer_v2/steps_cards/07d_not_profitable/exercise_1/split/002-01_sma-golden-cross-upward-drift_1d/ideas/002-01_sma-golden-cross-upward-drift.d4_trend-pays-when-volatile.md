---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's short moving average is above its long one, the coin rises more on days when its recent volatility is high than on calm days.
Consequence: A trader should hold the trend long mainly in volatile stretches and treat calm up-signal days as exposure that earns nothing.
Why:
- F11: Calm in-position days earn little: the book makes 0.00029 a day in the calmest third against 0.00254 in the most volatile third. The coin returns −0.00028 and 0.00273 a day in those same thirds.
- F12: The tails nearly cancel out. The 10% of in-position days with book returns below −5% sum to −110.7, against +120.7 from days above +5%. All in-position days together sum to only +13.9.

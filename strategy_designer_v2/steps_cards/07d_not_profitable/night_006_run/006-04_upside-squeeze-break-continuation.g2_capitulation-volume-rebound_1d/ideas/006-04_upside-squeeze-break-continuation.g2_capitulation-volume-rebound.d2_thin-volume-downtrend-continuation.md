---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin has fallen over the last 5 days while trading below its 50-day average close, the lower its 5-day average volume against its 30-day average, the further it keeps falling over the next 3 days.
Consequence: A thin-volume decline inside a downtrend is a reason to stay short or out rather than buy the dip.
Why:
- F2: The forecast is never below about +5, so the book is always long in the falling regime (about 49% of bars, average allocation 0.50). Its lowest-forecast third loses (gain -0.000262 per bar, next-day coin return -0.00199). Only its top third pays (gain 0.001242, coin return +0.00245).
- F3: On the 3-day grid, the volume-ratio effect sits above the coin's 50-day average. There the excess 3-day return rises from -0.0085 to +0.0075 to +0.0158 (t 2.39, n 149) across forecast thirds, with slope t 2.53 (n 551). Below the 50-day average all three thirds are negative (-0.0065, -0.0065, -0.0008) and the slope t is only 1.77 (n 1037).
- F5: When the coin is between 13% and 3% below its 50-day average (second sma quintile), falling coins underperform their average by 1.29% over the next 3 days (t -2.85, n 317). The book is long in exactly that falling-market state.

---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin has fallen over the last 5 days, the higher its 5-day average volume against its 30-day average, the larger its rebound over the next 3 days, only while its close is above its 50-day average close.
Consequence: A trader buys high-volume dips only inside an uptrend and stays out of high-volume falls that are part of a larger decline, which is where the book's deep falls come from.
Why:
- F1: The book earns 0.000074 a day (Sharpe 0.10) against 0.00118 a day (Sharpe 0.55) for holding the coins, and its chained value falls by as much as 56%. All of its mean bar gain of 0.000218 comes from the market's own rise (0.000288), while its timing is negative (-0.000072).
- F3: On the 3-day grid, the volume-ratio effect sits above the coin's 50-day average. There the excess 3-day return rises from -0.0085 to +0.0075 to +0.0158 (t 2.39, n 149) across forecast thirds, with slope t 2.53 (n 551). Below the 50-day average all three thirds are negative (-0.0065, -0.0065, -0.0008) and the slope t is only 1.77 (n 1037).
- F4: The four worst windows (w14, w2, w7, w13) carry the falls. Their losses come almost entirely from bars below the 50-day average: a gain sum of -1.94 over 842 active bars, against -0.20 over 132 bars above it. In the other windows both states earn (+3.34 below, +2.03 above).
- F5: When the coin is between 13% and 3% below its 50-day average (second sma quintile), falling coins underperform their average by 1.29% over the next 3 days (t -2.85, n 317). The book is long in exactly that falling-market state.

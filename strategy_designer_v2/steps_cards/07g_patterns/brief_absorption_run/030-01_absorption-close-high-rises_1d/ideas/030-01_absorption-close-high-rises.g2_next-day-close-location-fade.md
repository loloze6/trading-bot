---
brief: 030_absorption-day-close-location
source-idea: 030-01_absorption-close-high-rises
line: 7.g patterns
backtest: 030-01_absorption-close-high-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Over the next day, a coin moves against where its previous daily close sat in that day's high-low range: the nearer the close was to the high, the lower the next day's return.
Consequence: A close near the day's high is a reason to refuse a next-day long, and a close near the low a reason to refuse a next-day short.
Why:
- F2: This one-day reversal grows with volume. The slope is -0.026 (t -1.51, n 8994) when volume is under its 20-day mean, -0.063 (t -2.25, n 4214) at 1-2x, and -0.285 (t -4.68, n 1292) at 2x or more. Across all days it is -0.066 (t -4.86, n 17379), and it stands out from the roughly 100 slopes and groups examined.

---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high against its 30-day volatility, its 24-hour return reverses over the next 24 hours, and the higher that ratio, the larger the reversal.
Consequence: A trader fades the last day's move mostly when the coin has just turned unusually volatile, and more as the volatility burst grows.
Why:
- F4: The 24h reversal is concentrated where 24h volatility is high against its 30-day level. It is +56.3 bp in the top quintile of vol24/vol720 (t 4.7, 2585 cases), against -14.8 to +15.6 bp in the other four (|t| below 1.8).
- F1: Over the next 24 hours a coin reverses its own 24-hour return, and the reversal grows with the size of that return. Measured on the 24-bar grid, the reversal rises from -4.9 bp in the smallest |24h return| quintile to +13.4 bp in the fourth and +64.3 bp in the largest (t 5.1, 2585 cases). Read as a slope, it is +52.6 bp per usual 24h move of |24h return| (t 8.9, 12926 cases).

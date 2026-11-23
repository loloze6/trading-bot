---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its usual 24-hour move, the more strongly its price moves the opposite way over the next 24 hours.
Consequence: After an unusually large 24-hour move a trader leans against it for the next day, more heavily the larger the move, and refuses to chase it.
Why:
- F1: Over the next 24 hours a coin reverses its own 24-hour return, and the reversal grows with the size of that return. Measured on the 24-bar grid, the reversal rises from -4.9 bp in the smallest |24h return| quintile to +13.4 bp in the fourth and +64.3 bp in the largest (t 5.1, 2585 cases). Read as a slope, it is +52.6 bp per usual 24h move of |24h return| (t 8.9, 12926 cases).
- F2: In the largest |24h return| quintile the reversal holds across the data. It is positive in every coin, from +50.9 bp in ETH to +86.5 bp in ZEC (t 1.5 to 3.2, about 435 cases each), and in 79 % of the 24 windows. Its strength is 0.13 of the coin's usual 24h move, well above the 0.05 typical of real ideas. Its total move of +63.6 bp is 3.3 times the 0.19 % cost of a trade.
- F7: The book lost through its shorts. Short trades averaged -0.41 % before fees against +0.23 % for longs (about 16000 trades each side). The book's daily mean was negative every year from 2022 to 2025 (-8.5 to -11.9 bp, t -2.6 to -3.8), for a Sharpe of -0.83.

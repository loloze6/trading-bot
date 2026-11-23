---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's 24-hour fall relative to its usual 24-hour move, the larger its rise over the next 24 hours.
Consequence: A trader buys a coin after a sharp one-day fall, sized by the depth of the fall, rather than shorting the weakness.
Why:
- F3: The reversal is lopsided by side. After the largest 24h falls the next 24h excess return is +96.9 bp (t 5.1, 1240 cases), against +34.2 bp of reversal after the largest 24h rises (t 2.1, 1345 cases).
- F1: Over the next 24 hours a coin reverses its own 24-hour return, and the reversal grows with the size of that return. Measured on the 24-bar grid, the reversal rises from -4.9 bp in the smallest |24h return| quintile to +13.4 bp in the fourth and +64.3 bp in the largest (t 5.1, 2585 cases). Read as a slope, it is +52.6 bp per usual 24h move of |24h return| (t 8.9, 12926 cases).
- F7: The book lost through its shorts. Short trades averaged -0.41 % before fees against +0.23 % for longs (about 16000 trades each side). The book's daily mean was negative every year from 2022 to 2025 (-8.5 to -11.9 bp, t -2.6 to -3.8), for a Sharpe of -0.83.

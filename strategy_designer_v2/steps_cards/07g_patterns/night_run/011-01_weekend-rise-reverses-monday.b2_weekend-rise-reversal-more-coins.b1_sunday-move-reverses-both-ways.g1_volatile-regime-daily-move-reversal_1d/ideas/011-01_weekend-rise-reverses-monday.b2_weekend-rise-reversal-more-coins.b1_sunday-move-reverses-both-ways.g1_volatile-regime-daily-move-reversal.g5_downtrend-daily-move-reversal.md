---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily move is followed by a move the other way over the next day, and the more the coin has fallen over the past 20 days, the larger the move back.
Consequence: A trader would fade daily moves harder in coins that have been falling over the past 20 days.
Why:
- F7: The fade works better in falling markets: when the coin's 20-day return is negative, the fade gain is 0.00160 (t 3.35, n 15538), against 0.00048 (t 1.11, n 14584) when it is positive.

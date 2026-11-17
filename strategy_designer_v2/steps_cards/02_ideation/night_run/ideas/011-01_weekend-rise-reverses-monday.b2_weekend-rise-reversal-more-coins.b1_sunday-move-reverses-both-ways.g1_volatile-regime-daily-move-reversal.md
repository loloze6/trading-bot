---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily move is followed by a move the other way over the next day, and the larger the move and the higher the coin's 20-day volatility, the larger the move back.
Consequence: A trader would fade a coin's daily move when its recent volatility is high, sizing up with both the move and the volatility, and would not fade moves in calm stretches.
Why:
- F1: Next-day reversal of a coin's daily move depends on its recent volatility. On all days, the slope of the next-day excess return on the standardised daily return is -22.1 bp per unit (t -5.9, n 10179) in each coin's top 20-day-volatility tercile, against +6.9 bp (t 2.2) in the bottom tercile. On weekdays alone it is -16.2 bp (t -3.8) in the top tercile against +10.3 bp (t 2.9) and +8.3 bp (t 2.2) in the lower two. In a weekday regression, the volatility-by-move interaction is -2.3 bp (t -2.34) while the plain move term is -1.4 bp (t -0.56).
- F2: The reversal is strongest on weekend days in high volatility. The slope is -51.1 bp per unit (t -6.5, n 2891) in the top volatility tercile, -21.2 bp (t -2.8) in the middle and -7.3 bp (t -1.1) in the bottom. The high-volatility weekday reversal is negative in 6 of 8 years, with t ≤ -2.4 in 5 of them.

---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_volatile-regime-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily move is followed by a move the other way over the next day, and the higher that day's volume relative to its 30-day median, the larger the move back.
Consequence: A trader would fade moves made on heavy volume more strongly than moves on quiet days.
Why:
- F4: Moves made on heavy volume reverse more, which is the opposite of the brief's thin-book claim: in the top tercile of the day's volume over its 30-day median the fade gain is 0.00170 (t 2.66, n 9145), against 0.00005 (t 0.11) in the bottom tercile.

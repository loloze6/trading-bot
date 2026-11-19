---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's fall over 2 hours, measured in its usual 2-hour moves, is followed by a rise over the next 1 hour. The rise grows with the size of the fall and is larger than what follows an equal rise.
Consequence: A trader should buy sharp short falls and hold them for about an hour, and fade sharp rises with much less size or not at all.
Why:
- F2: The reversal is lopsided. In the bottom decile of the 2-hour move (big falls, mean z -2.74), the next 2 hours return +12.3 bp in excess (t 8.2, n 19950). In the top decile (big rises, mean z +2.75), they return only -3.7 bp (t -2.9). In that falls decile, 8.4 bp of the fade comes in the first hour against 4.9 bp in the second, which contradicts the idea's claim that most of the reversal comes in the second hour.
- F1: The book's gross gain before costs is 0.97 bp per bar, while fees cost 4.34 bp per bar on a turnover of 0.40 of the book per bar, so the mean daily book return is -80.4 bp against the coins' +11.9 bp over 17381 coin-days; the edge that was confirmed is real but far too thin for hourly rebalancing.

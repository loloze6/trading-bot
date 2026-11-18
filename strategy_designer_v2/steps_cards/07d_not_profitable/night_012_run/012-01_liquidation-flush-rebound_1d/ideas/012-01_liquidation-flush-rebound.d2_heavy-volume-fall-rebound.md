---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-01_liquidation-flush-rebound
line: 7.d not profitable
backtest: 012-01_liquidation-flush-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close falls by at least its usual 20-day move on volume far above its own 30-day average volume, price rises over the next 3 days; the larger the volume over its 30-day average, the larger that rise.
Consequence: Heavy-volume sharp falls, with or without a wick, are a more frequent reason to buy for a 3-day rebound, and the heavier the volume the stronger that reason.
Why:
- F3: The situation is too rare for the book to work: trades per bar are 0.0091, and the book holds a position on only 321 of 17524 coin-days.
- F4: Across all falls of at least one usual move (n 1642), the 3-day excess return grows with the volume burst: by volume-ratio quartile it is -0.0040, 0.0027, 0.0002 and 0.0188, and the top quartile (mean ratio 3.06, n 411) holds most of the gain (Spearman 0.053).
- F5: The long lower wick works against the rebound rather than for it: across the same falls, the 3-day excess return falls from 0.0141 in the shortest-wick quartile to -0.0002 in the longest (Spearman -0.072).

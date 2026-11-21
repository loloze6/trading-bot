---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves
line: 7.b inconclusive
backtest: 022-03_combined-extremes-larger-moves_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 1-day return, scored against its past 365 days and weighted by how well it predicted the following 5 days' return over those 365 days, is far from its usual value, the coin moves in that term's direction over the next 20 days, and the further out the term, the larger the move.
Consequence: A trader would hold a position on the past-weighted 1-day reversal signal for about 20 days instead of 5, where its move per case is far larger than a round trip's cost.
Why:
- F5: The one clear, graded effect in this data is the past-weighted 1-day reversal term over 20 days, not 5. Its top-10% cells give a signed unusual move of +8.6 % (t 4.07, 79 non-overlapping cases), on both sides: long +7.8 % (t 2.15, 40 cases) and short +9.4 % (t 4.34, 39 cases). Its slope on all 788 cells has t 2.49, and its top minus bottom quintile is +8.5 % (Welch t 3.46). At 5 days the same term is weak (top-10% t 0.90; long side +1.8 %, t 2.20). Its move per case is about 45 times the 0.19 % cost of a trade. The case count is small and the size is unusually large next to F10's usual 0.05 strength, so it needs testing on more coins.
- F1: The combined score's rarest readings do not lead to larger moves than a single effect's. On its top-10% cells the signed unusual 5-day move is -0.38 % (t -0.55, 326 cases). The best single, the reversal term, gives +0.56 % (t 0.90, 326 cases). Combined minus best single is -0.94 % (Welch t -1.01), on the side opposite to the idea's. The size is 0.002 of the coin's usual move, against the usual 0.05 (findings F10), and the total move is -0.2 times the 0.19 % cost of a trade (findings F11).
- F2: The combined score is not graded and its sign tends to point the wrong way. Its absolute-value deciles give signed unusual moves of -1.5 % to +0.2 %, with no trend (the top decile is -0.38 %). Its slope on all 3,254 cells has t -1.97 at 5 days, -1.36 at 1 day and -1.90 at 10 days. Its all-cells correlation with the unusual move is -0.035. The weights learned from the past year do not carry forward, which is one of the brief's own ways of being wrong.

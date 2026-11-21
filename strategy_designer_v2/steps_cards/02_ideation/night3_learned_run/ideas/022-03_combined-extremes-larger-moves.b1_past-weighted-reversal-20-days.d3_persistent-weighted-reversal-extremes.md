---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days
line: 7.d not profitable
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 1-day return, scored against its past 365 days and weighted by how well it predicted the following 5 days' return over those 365 days, is far from its usual value, the coin moves in that term's direction over the next 20 days, and the further out the term, the larger the move. The move is larger the more days of the past 20 days the term has stayed far out on the same side.
Consequence: A trader would act on an extreme of the term that has lasted, not on one that has just appeared, which is where the fresh-entry trades lost more than a round trip's cost.
Why:
- F7: The term pays when an extreme is read on the grid, not when it first appears.
- F1: The short side causes every failed measure. Shorts held for 13,447 bars and lost a mean -0.177 % per bar; longs held for 12,029 bars and gained +0.136 % per bar. Summed bar gains are -23.8 for shorts and +16.4 for longs. Closed trades after fees average -25.3 % on 1,340 shorts and +12.1 % on 994 longs.

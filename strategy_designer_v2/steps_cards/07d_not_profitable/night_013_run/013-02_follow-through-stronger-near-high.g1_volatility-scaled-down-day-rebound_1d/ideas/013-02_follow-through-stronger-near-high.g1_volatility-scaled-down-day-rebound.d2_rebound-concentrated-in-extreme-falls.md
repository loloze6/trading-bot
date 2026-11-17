---
brief: 013_anchoring-to-recent-high
source-idea: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound
line: 7.d not profitable
backtest: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's fall on a day, measured against its own volatility over the previous 20 days, is followed by a rise over the next 1 day, with the rise growing faster than in proportion to the scaled fall, so that ordinary falls are followed by a weaker day than the coin's usual and only falls of several usual moves by a strong rebound.
Consequence: A trader buys only after the deepest volatility-scaled falls, which removes most of the small trades whose fees exceed their gain.
Why:
- F2: The gain sits only in the largest scaled falls: on active bars where the coin fell over 60 days, the two lowest forecast quartiles have next-day excess returns of -0.00147 and -0.00080 and gross gains of -0.00001 and 0.00009, yet still pay fees of 0.00018 and 0.00029, while the top quartile earns an excess of +0.00623 (gross 0.00494); the 20-day split shows the same, -0.00087 and -0.00136 in the two lowest quartiles against +0.00504 in the top one.
- F1: Fees take 0.000349 of the 0.000804 gross gain per coin per bar, about 43%, at a turnover of 0.33 of the book per bar; the 7100 trades last 1.8 days on average and lose 0.34% before fees and 0.44% after, so the book's mean daily return is 0.000446, below the 0.0005 bar and below holding's 0.00118.
- F4: The book's deepest fall is -30.7% over 120 days, from w8 into w9, and w9 is its worst window at -0.0013 per day; the 30 worst book days average -8.0%, came with a prior position of 0.81 of the book, and followed a 20-day coin return of -16.8%.

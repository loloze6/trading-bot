---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return, the larger the gain.
Consequence: Read nearness to the high as a long signal only when the past month has risen, which also removes the short positions that paid for the market's rise.
Why:
- F3: The short side lost money. Short bars earned a daily gain of -0.000048, because the coin still rose 0.00079 a day while the book was short. That was a market-rise cost of -0.000156, which only partly offset a timing gain of +0.000108. Long bars earned +0.00036.
- F4: Near the high (top 20 % of distance), the following day depended on the coin's 30-day return:
- F6: The falls were large against the gain. The chained book's deepest fall was -16.7 % against a yearly return of 3.9 % (Calmar 0.23). Windows w16 to w24 held the seven deepest falls, at -12 % to -17 %.

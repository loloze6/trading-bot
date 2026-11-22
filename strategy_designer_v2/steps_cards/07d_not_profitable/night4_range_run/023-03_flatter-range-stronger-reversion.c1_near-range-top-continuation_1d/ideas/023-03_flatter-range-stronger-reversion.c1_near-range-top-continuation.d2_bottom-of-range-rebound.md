---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to the bottom of its 30-day closing range, the more the coin rises over the next 10 days.
Consequence: A close pressed against the bottom of the past month's range is a reason to buy the rebound over the following days rather than to sell it.
Why:
- F3: Below the middle of the range the coin rises back rather than falling further, so the shorts bet the wrong way.
- F4: The deepest fall, which fails the Calmar test (0.206), was driven by the shorts.

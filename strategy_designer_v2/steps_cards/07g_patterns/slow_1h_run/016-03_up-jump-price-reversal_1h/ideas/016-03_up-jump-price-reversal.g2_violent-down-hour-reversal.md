---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's latest hourly fall relative to its past week's typical hourly move, the more the coin rises over the next 24 hours.
Consequence: A violent down hour is a reason to buy for the next day rather than to follow the move down.
Why:
- F3: Large down hours reverse over the next day. On the non-overlapping 24-hour grid, the lowest septile of the hour's return scaled by its 168-hour volatility is followed by +0.00692 over 24 hours (t 6.13, n 2320), against -0.0016 after the top septile. Inside down hours the 24-hour rise falls from 0.00677 to 0.00344 to 0.00142 across the first three quintiles, and the pooled slope is -0.0018 (t -2.60, n 8177). This is clear in XRP (t -2.55) and ZEC (t -2.83) only.

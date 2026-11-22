---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 8 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend, and the stronger the 24-hour trend, the larger the move back.
Consequence: A trader takes the reversal bet at settlement only when the move into settlement goes against the recent trend, and sizes it by the trend's strength, holding it through the 8 hours to the next settlement.
Why:
- F1: The move per case is far too small to pay for a trade, so the book loses before any choice of sizing. The idea's total move is +0.05 % per case over 2 hours, which is 0.2 times the 0.19 % cost of a trade. The book made 65 566 trades, a median of 120 minutes each, averaging −0.078 % before fees and −0.178 % after. Sharpe was −3.97, the mean daily return on days in a position −0.2 %, and the yearly return −51.9 %.
- F4: The 08:00 UTC settlement carries none of the effect.
- F5: The move reverses when it runs against the coin's 24-hour trend, the crowded-side reading the brief gives, and it grows with the strength of that trend.
- F8: The book's gross gain sits entirely in the first 2 hours after settlement, at +0.38 and +0.75 bp per bar with a mean |allocation| of 0.43. The other six hours hold about 0.014 and earn about 0. The book pays the full cost every 8 hours for a 2-hour move, and that move is below the cost.

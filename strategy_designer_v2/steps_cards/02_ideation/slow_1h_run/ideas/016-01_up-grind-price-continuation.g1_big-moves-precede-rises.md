---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation
line: 7.g patterns
backtest: 016-01_up-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's absolute 3-day return, whether up or down, the more the coin rises over the next 3 days.
Consequence: After a big 3-day move in either direction, a trader leans long, and harder the bigger the move; after a quiet 3 days they hold back.
Why:
- F1: The size of a coin's 3-day move, in either direction, carries the next 3 days' rise. On the non-overlapping 72-bar grid, the largest third of 3-day moves was followed by a mean next-72-bar return of +0.0124 after rises (t 3.82, n 978) and +0.0090 after falls (t 2.82, n 869). The smallest third gave +0.0005 after small rises (t 0.19) and -0.0046 after small falls (t -1.92). In a pooled regression on standardised values, the 3-day move's absolute size has a beta of 0.0050 (t 4.38) and its signed value a beta of -0.0067 (t -2.73).
- F3: The tested grind share mostly measures the move's size, and the book lost money. Across up-move terciles of the share, the next-72-bar return rises from -0.0010 to +0.0039 to +0.0126, but the past 3-day rise grows with it, from 0.015 to 0.053 to 0.112. At the forecast's own split the top-minus-bottom difference is -0.0043 (Welch t -0.57, 316 cases per third). The book's mean daily return was -0.000522, against +0.00119 for holding the coins.

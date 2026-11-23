---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 24 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader holds the settlement-fall rebound for a day to spread one trade's cost over a larger move.
Why:
- F1: The book's gain is eaten by its fees: over all bars it earns 0.183 bp per bar before costs and pays 0.178 bp per bar in fees, with the fees landing on the entry bar (2.12 bp at the 16:00 close) and the exit bar (2.05 bp eight hours later), so a Sharpe of -0.02 and a yearly return of -2.0 % follow from a move per case (+0.23 % total) only 1.2 times the 0.19 % cost of a trade.
- F2: Most cases are too small to pay: at the 16:00 close the 8-hour return after a fall is +0.086 % (t 1.1, n 1153) for forecasts up to 2 and +0.089 % (t 1.3, n 1607) for forecasts 2 to 5, both below the 0.19 % cost; it is +0.42 % (t 6.5, n 2111) for forecasts 10 to 20; and the two smallest fall quintiles give +0.07 % and +0.04 % (t 1.2 and 0.5) against +0.48 % and +0.30 % (t 6.5 and 3.2) for the two largest.
- F5: In the high-volatility tercile the large-fall rebound keeps building past 8 hours, to +0.82 % over 24 hours (t 5.0, n 1577), 4.3 times the cost of a trade, against +0.06 % and +0.09 % over 24 hours in the low and middle terciles (t 0.4 and 0.6) and +0.11 % (t 1.1) after rises in high volatility.

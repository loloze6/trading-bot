---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's up day relative to its own 20-day volatility, the larger its return over the next 5 days.
Consequence: An unusually large up day is a reason to buy for the following week, with a move per case several times a trade's cost.
Why:
- F3: A large up day is followed by a further rise. After a 1-day return of 1 to 2 times the coin's 20-day volatility, the next 5 days run +1.55 % above the coin's mean (t 2.38, 286 cases), and above 2 times, +2.58 % (t 1.76, 94 cases). Large down days show no matching fall (+0.12 % and +0.02 %). The slope stays positive once the 28-day return is controlled for (z1 t 2.04, with r28z t 2.42, 2555 cases), and it is positive on all 6 coins (XRP t 2.24, ZEC t 1.70). Per case it is about 8 times the 0.19 % cost of a trade.

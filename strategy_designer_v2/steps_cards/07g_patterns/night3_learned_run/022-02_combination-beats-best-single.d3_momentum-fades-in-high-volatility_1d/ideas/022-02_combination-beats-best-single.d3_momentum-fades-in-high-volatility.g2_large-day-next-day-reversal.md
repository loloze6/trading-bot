---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day return against its 30-day daily volatility, the more its return over the next day goes the opposite way.
Consequence: A trader should lean against a coin's unusually large daily moves for one day, and avoid chasing them.
Why:
- F5: A coin's one-day move reverses the next day, and the reversal grows with the move. The 1-day volatility-scaled return times the next day's excess return has t -4.19 (14,500 days), negative on all 6 coins. The reversal is 10, 11 and 28 bps per case from the smallest to the largest third of moves. In the largest third it is positive on all 6 coins (6 to 64 bps), with t 3.76 in w1 to w12 and t 1.81 in w13 to w24. At 28 bps it is only about 1.5 times the cost of a round trip.

---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's close sits to its highest close of the past 60 days, the higher its return over the next 20 days.
Consequence: A trader should lean long on coins pressing their 60-day highs and refuse longs on coins far below them, holding for about three weeks.
Why:
- F7: Nearness to the 60-day high carries a 20-day move the momentum lacks. Cases closer than the coin's median to their 60-day high, against those farther, gave a signed unusual move of +3.59 % per 20 days (t 2.97, 395 cases), about 19 times the 0.19 % cost of a trade.
- F4: The book's short side destroys what its long side earns. Long bars summed +12.18 of gain before costs over 8198 bars, short bars -5.96 over 9124 bars. Short trades averaged -6.12 % net with 31 % winners (2146 trades), long trades +10.82 % net with 49 % winners (1506 trades).
- F1: The tested momentum does not predict the next 20 days. The rank correlation of the volatility-scaled 28-day return with the 20-day unusual move is 0.03, and its signed unusual move is -0.33 % per case (t -0.34, 539 cases). Its quintiles do not rise in order: -1.58 %, -1.45 %, +3.35 %, -1.67 %, +0.64 %. Its size, -0.44 % per case, is below zero, so no holding, sizing or threshold can bring it over the 0.19 % cost.

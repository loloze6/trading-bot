---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 20 days, the more so the closer its close sits to its highest close of the past 60 days.
Consequence: Momentum bets held for weeks should be sized by how near the coin is to its recent high rather than by its calm, and cut when the coin trades far below that high.
Why:
- F7: Nearness to the 60-day high carries a 20-day move the momentum lacks. Cases closer than the coin's median to their 60-day high, against those farther, gave a signed unusual move of +3.59 % per 20 days (t 2.97, 395 cases), about 19 times the 0.19 % cost of a trade.
- F1: The tested momentum does not predict the next 20 days. The rank correlation of the volatility-scaled 28-day return with the 20-day unusual move is 0.03, and its signed unusual move is -0.33 % per case (t -0.34, 539 cases). Its quintiles do not rise in order: -1.58 %, -1.45 %, +3.35 %, -1.67 %, +0.64 %. Its size, -0.44 % per case, is below zero, so no holding, sizing or threshold can bring it over the 0.19 % cost.
- F2: The volatility condition runs against the idea. In the calmest third of 30-day volatility against its own past, signed momentum lost 2.53 % per 20 days (t -1.25, 180 cases); the middle third gained 1.15 % (t 0.91) and the wildest third 1.19 % (t 0.73).
- F5: The failing Calmar of 0.066 comes from a deep, long fall. The chained pooled book reached falls of -59 % to -65 % through windows 5 to 10, while its mean daily return there was between -0.0015 and +0.0026.

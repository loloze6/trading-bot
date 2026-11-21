---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
line: 7.b inconclusive
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 60-day return, the more the coin moves in that same direction over the next 10 days, only while the coin's 30-day volatility is high against its own past.
Consequence: If confirmed, a trader would follow a coin's 60-day trend for about ten days when the coin is volatile, and would not rely on it when the coin is calm.
Why:
- F1: The 60-day trend's effect is on the side the idea predicts but weakens past 10 days. On each horizon's non-overlapping grid, the forecast-weighted unusual move has t 2.14 over 5 days (6,627 cases) and t 2.46 over 10 days (3,280 cases), against t 1.13 over 20 days (1,606 cases, the test's own measure), t 0.64 over 40 days and t 0.90 over 60 days. Strength is 0.048 over 10 days against 0.033 over 20 days.
- F3: The 20-day effect is absent when the coin is calm and shows only when it is volatile. In the lowest tercile of each coin's own 30-day volatility, the unusual move is +0.27 % (t 0.24, strength 0.018, 439 cases). In the middle tercile it is +3.07 % (t 2.18, strength 0.107), and in the highest +3.50 % (t 1.58, strength 0.087). Over 10 days the highest tercile carries the strongest effect: +2.00 %, t 2.53, strength 0.102, Spearman 0.061, about twice the lower terciles' 0.056 to 0.058.
- F6: The size is large enough to pay if the effect were firm. Over 20 days the total move is +0.93 % per case, 4.2 times the 0.22 % cost of a buy and a sell. Over 10 days it is +0.86 %, about 3.9 times. Little more data is available: the test already used all 15 coins and all four folds, and the remaining coins have only fold D.

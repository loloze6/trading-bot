---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
line: 7.b inconclusive
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 60-day return, the more the coin moves in that same direction over the next 10 days.
Consequence: If confirmed, a trader would have a reason to hold longs and refuse shorts for about ten days after a coin's large 60-day rise, and the reverse after a large fall.
Why:
- F1: The 60-day trend's effect is on the side the idea predicts but weakens past 10 days. On each horizon's non-overlapping grid, the forecast-weighted unusual move has t 2.14 over 5 days (6,627 cases) and t 2.46 over 10 days (3,280 cases), against t 1.13 over 20 days (1,606 cases, the test's own measure), t 0.64 over 40 days and t 0.90 over 60 days. Strength is 0.048 over 10 days against 0.033 over 20 days.
- F2: Over the tested 20 days the idea has almost no grading. The Spearman correlation between the forecast and the coin's unusual 20-day move is -0.010. Across the abs(forecast) quartiles the mean unusual move runs 0.47 %, 2.02 %, 1.71 %, 0.70 %, so the largest quartile is no better than the smallest; this is why the supporting check fails (-0.036 %). Over 10 days the largest abs(forecast) quartile carries the most: 1.41 %, t 2.15, strength 0.079, against 0.17 % to 1.10 % in the other three.
- F6: The size is large enough to pay if the effect were firm. Over 20 days the total move is +0.93 % per case, 4.2 times the 0.22 % cost of a buy and a sell. Over 10 days it is +0.86 %, about 3.9 times. Little more data is available: the test already used all 15 coins and all four folds, and the remaining coins have only fold D.

---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive, and the more times that level turned the price down and the farther the close sits above it, the larger the rise, the move showing mainly in the breaks that clear the most-defended levels by the widest margin.
Consequence: A trader would buy only the clearest breaks of the most-defended levels in a rising quarter, and refuse the marginal breaks that make up most of the signals.
Why:
- F1: The tested effect is on the predicted side but small and skewed. The 5-day excess return is +0.43 % per case with t 1.42 over 2511 cases, a strength of only 0.031 against F10's usual 0.05. The median case is -1.17 % and only 43 % of cases end above the coin's normal drift, so the mean rests on a minority of large rises.
- F2: The effect sits in the strongest forecasts only, and the test's unweighted mean dilutes it. By forecast quartile the 5-day excess is -0.27 % (t -0.58), -0.52 % (t -1.10), +0.64 % (t 0.83) and +1.82 % (t 2.90, 637 cases). The top quartile has a strength of 0.149, about 3 times the usual 0.05. The rank correlation of forecast with outcome over all cases is only 0.026.
- F3: Of the forecast's two parts, the break reading (touch count × margin above the level) separates most sharply. Its top quartile gains +2.14 % over 5 days (t 2.44, 645 cases); the three lower quartiles gain -0.36 %, -0.09 % and +0.03 %, all with |t| < 0.8. The 10-day run grades less cleanly: its quartiles give -0.54 %, -0.19 %, +1.44 % and +0.96 %, and the top is no better than the third.
- F7: Size covers the cost. The total move per case (+1.17 %) is 5.2 times the 0.22 % round trip and the unusual move 1.9 times. In the strongest breaks the unusual move is about +1.8 to +2.1 %, roughly 8 to 10 times the cost. The test already used all 19 coins on all four folds, so no more daily data is available.

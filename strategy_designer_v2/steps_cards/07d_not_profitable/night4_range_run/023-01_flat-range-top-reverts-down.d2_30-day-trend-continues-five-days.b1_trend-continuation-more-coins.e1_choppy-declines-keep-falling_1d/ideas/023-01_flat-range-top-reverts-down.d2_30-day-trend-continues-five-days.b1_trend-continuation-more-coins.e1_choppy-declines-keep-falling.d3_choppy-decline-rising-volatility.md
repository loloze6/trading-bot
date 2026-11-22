---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin that has fallen over the past 30 days while its 30-day net move stayed small against its 30-day high-low range, the further the coin keeps falling over the next 5 days, the higher its 30-day volatility stands against its 60-day volatility.
Consequence: A trader would size shorts on choppy declines by how much volatility has expanded, and skip them in quiet, contracting markets.
Why:
- F1: The book fails on its gain. Its mean daily return is -0.0066 % a coin-day, and -0.0053 % before fees. Holding's own rise takes -0.0108 % a day, because the book is short on 52 % of days in coins whose normal 5-day drift is positive for all 19 coins. Timing adds back only +0.0043 %. The total move per case is +0.13 %, 0.6 times the 0.22 % cost of a trade.
- F2: The forecast's strength does not grade the move. Grid short bars by forecast quartile, strongest to weakest, give total moves of +0.19 %, +0.43 %, -0.14 % and -0.08 % (t 0.35, 0.91, -0.28, -0.17, about 464 cases each). Trades lose in every entry-forecast quartile, from -0.99 % to -3.12 % net, over 3225 trades.
- F6: The fall pays more when volatility is high and rising. In the top quartile of 30-day volatility, the total move is +1.56 % (t 2.59), against -0.45 % in the bottom quartile. In the top quartile of 30-day over 60-day volatility, it is +1.78 % (t 2.79).

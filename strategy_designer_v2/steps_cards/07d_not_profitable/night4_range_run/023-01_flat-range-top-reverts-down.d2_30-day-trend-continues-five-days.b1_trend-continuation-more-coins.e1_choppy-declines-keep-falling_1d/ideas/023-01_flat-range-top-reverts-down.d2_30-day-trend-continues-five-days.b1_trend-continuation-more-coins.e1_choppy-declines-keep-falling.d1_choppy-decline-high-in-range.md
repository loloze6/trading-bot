---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin that has fallen over the past 30 days while its 30-day net move stayed small against its 30-day high-low range, the higher its close sits within that 30-day range, the further the coin falls over the next 5 days.
Consequence: A trader would short a choppy declining coin when it has bounced toward the top of its 30-day range, not when it is already sitting near the bottom.
Why:
- F1: The book fails on its gain. Its mean daily return is -0.0066 % a coin-day, and -0.0053 % before fees. Holding's own rise takes -0.0108 % a day, because the book is short on 52 % of days in coins whose normal 5-day drift is positive for all 19 coins. Timing adds back only +0.0043 %. The total move per case is +0.13 %, 0.6 times the 0.22 % cost of a trade.
- F2: The forecast's strength does not grade the move. Grid short bars by forecast quartile, strongest to weakest, give total moves of +0.19 %, +0.43 %, -0.14 % and -0.08 % (t 0.35, 0.91, -0.28, -0.17, about 464 cases each). Trades lose in every entry-forecast quartile, from -0.99 % to -3.12 % net, over 3225 trades.
- F3: Losses come from sharp rebounds against the short. The book's daily returns correlate -0.56 with the coin. The coin rose +14.0 % on average on the book's worst 1 % of days, and those days sum to 3.8 times the book's whole net result. The worst 5 % of trades lose 26.6 % or more, and the trade mean is -2.0 % with them but +1.05 % without them.
- F4: The fall pays where the coin closes high in its 30-day range. In the top quartile of position in the 30-day high-low range (above 0.51), the total move is +1.64 % (t 3.02) and the unusual move +2.42 % (t 4.44), over 339 cases. The three lower quartiles give total moves of +0.37 %, -0.19 % and -0.27 %.

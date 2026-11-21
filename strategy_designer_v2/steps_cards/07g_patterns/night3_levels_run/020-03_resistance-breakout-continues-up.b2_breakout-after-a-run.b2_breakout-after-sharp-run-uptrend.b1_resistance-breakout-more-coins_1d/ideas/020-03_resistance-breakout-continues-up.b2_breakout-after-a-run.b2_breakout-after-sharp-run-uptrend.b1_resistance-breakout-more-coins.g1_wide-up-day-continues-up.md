---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes up on a day whose high-to-low range is wide compared with its ranges over the past 20 days, it tends to rise over the next 5 days, and the wider that day's range relative to its 20-day average, the larger the rise.
Consequence: A wide up-closing day is a reason to buy for the following week, and a narrow, quiet day is a reason to refuse a long.
Why:
- F1: A day whose high-to-low range is wide against the coin's own last 20 days is followed by a larger 5-day rise. The widest quintile gives +1.56 % excess over the coin's normal 5-day drift, a strength of 0.111, over 1251 non-overlapping cases. That excess is positive in 19 of 19 coins and in 71 % of the windows, with a window-clustered t of 1.73. The relation is graded: the per-coin Spearman rho has a median of 0.083 and is positive in 17 of 19 coins, and the two narrowest quintiles give -0.79 % and -0.97 %.
- F2: The wide-range effect is strongest when the day closes up. Wide days that close up give +2.33 % 5-day excess (strength 0.142, 592 cases). Wide days that close down give +0.88 % (strength 0.083, 663 cases). All other days give -0.53 % to -0.57 % (about 5,000 cases). The +2.33 % is about 10 times the 0.22 % round-trip cost of this backtest.

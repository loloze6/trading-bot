---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's 30-day return compared with its volatility over those 30 days, the larger its rise over the next six days.
Consequence: Hold the coins whose past month rose most steadily and refuse longs in coins whose past month fell moderately.
Why:
- F2: The coin's 30-day return sets the sign of what follows any break, up or down. When the 30-day return is negative, both a break below the two-day low and a break above the two-day high are followed by underperformance over 6 days: -0.87 % (t -3.46, 2230 cases) and -0.99 % (t -3.33, 1634 cases).
- F3: On all bars, read once per 6-day grid cell, the 30-day return scaled by the coin's volatility grades the next 6 days from its second quintile up. By per-coin quintile, the unusual move is -1.55 % (t -3.66), -0.28 %, +0.58 % and +1.19 % (t 2.40), about 900 cases each. The lowest quintile breaks the order at -0.37 % (t -0.91). Over 3 days the same quintiles run from -0.87 % (t -4.75) to +0.75 % (t 2.96).
- F7: The breakout effects turn in bear years. In 2018 the downward break in a rising coin gives -5.8 % (t -5.2) and in 2022 -2.1 % (t -3.3). The upward break over 6 days gives -4.1 % (t -2.3) in 2018 and -2.0 % (t -2.5) in 2022. The book earns 0.028 % a day against 0.10 % to 0.48 % a day for holding, coin by coin, so most of the drift is left on the table.

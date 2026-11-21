---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The wider a coin's two-day range compared with its 30-day average 4h range, the more the coin rises over the next three days.
Consequence: Favour longs after wide recent ranges and refuse them after unusually narrow two-day stretches.
Why:
- F4: The width of the past two days' range, compared with the coin's 30-day average 4h range, grades the next 3 days on all bars, with no break needed. Spearman rho is 0.051 (p 1e-7, 10636 cases), the bottom quintile gives -1.02 % and the top +0.47 %. Rho is positive in 18 of 19 coins. In rising coins the quintiles run from -0.62 % to +0.94 %. The effect is strongest in 2021 (rho 0.18); in other years rho is -0.03 to 0.07, with 2023 and 2024 significant.
- F5: In the tested downward break in a rising coin, the width carries the edge. The two narrowest quintiles give -0.30 % and -0.53 % over 3 days. The two widest give +1.53 % (t 3.56) and +1.83 % (t 3.32). Wider minus narrower is positive in all 8 years.

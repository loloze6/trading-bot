---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend.b1_breakdown-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a 4h close rises above the highest high of the coin's preceding two days while the coin's 30-day return is positive, the coin rises more than usual over the next six days. The wider the two-day range was compared with the coin's 30-day average 4h range, the larger the rise.
Consequence: In a coin up over the past month, buy a break above a wide two-day range and hold it for days rather than hours.
Why:
- F1: An upward break in a rising coin keeps paying for longer than the tested downward break. After a 4h close above the highest high of the prior two days, with a positive 30-day return, the unusual move grows with the horizon: +0.20 % over 1 day (t 2.20, 4392 cases), +0.56 % over 3 days (t 2.69, 3090 cases) and +1.29 % over 6 days (t 3.47, 2169 cases). The tested downward break in a rising coin fades over 6 days: +0.35 % (t 3.23), then +0.56 % (t 2.73), then +0.37 % (t 1.15, 1569 cases). At 6 days the upward break's unusual move is about 5.9 times the 0.22 % cost of a trade.
- F4: The width of the past two days' range, compared with the coin's 30-day average 4h range, grades the next 3 days on all bars, with no break needed. Spearman rho is 0.051 (p 1e-7, 10636 cases), the bottom quintile gives -1.02 % and the top +0.47 %. Rho is positive in 18 of 19 coins. In rising coins the quintiles run from -0.62 % to +0.94 %. The effect is strongest in 2021 (rho 0.18); in other years rho is -0.03 to 0.07, with 2023 and 2024 significant.
- F5: In the tested downward break in a rising coin, the width carries the edge. The two narrowest quintiles give -0.30 % and -0.53 % over 3 days. The two widest give +1.53 % (t 3.56) and +1.83 % (t 3.32). Wider minus narrower is positive in all 8 years.

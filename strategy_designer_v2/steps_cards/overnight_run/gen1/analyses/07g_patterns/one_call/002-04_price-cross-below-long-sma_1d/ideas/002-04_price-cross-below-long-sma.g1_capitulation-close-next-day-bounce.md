---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily drop larger than twice the coin's recent daily volatility that closes near the day's low, the coin rises on the next day more often than not.
Consequence: A trader should refuse new shorts, or take a one-day long, after a high-volatility down day that closes at its low.
Why:
- F1: A daily drop of more than 2 of the coin's 20-day standard deviations that closes in the lowest fifth of its high-low range is followed by a next-day mean return of +1.36% (up 64.7%, t 3.91, n 272). The same drop closing in the upper half is followed by -1.08% (up 40%, n 30, t -1.12). All large drops together give +0.76% the next day (up 61%, t 2.85) against +0.13% for all bars. The up share after these drops is above 0.5 in every year (0.52 to 0.71), but the mean is clearly positive only in 2020 to 2021 (t 3.3 and 2.5).
- F2: Next-day return falls steadily as the day's own return rises. The coin's bottom daily-return decile is followed by +0.90% (up 60.9%, t 6.0), the second decile by +0.26% (t 2.1), and deciles 4 to 9 by between -0.07% and +0.05% with up shares from 0.445 to 0.49.
- F6: The book's worst 5% of days came after a coin down day averaging -2.2% (59% of them down days). Its best 5% came after a flat day (+0.09%). At both tails the short was about equally deep (allocation about -1.5, distance about -37%), which matches F1: shorts held into a fresh drop lose on the rebound.

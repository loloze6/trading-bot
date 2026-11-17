---
line: 7.d not profitable
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
idea tested: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4447 USD
---
## Findings
- **F1:** The short side is what sinks the book; the long side is not the problem. Short bars lost 0.000403 a day over 8894 bars, while long bars gained 0.001251 a day over 7906 bars. On the pooled daily chain, the short leg alone has a Sharpe of -0.29, a deepest fall of -0.76 and a Calmar of -0.13. The long leg alone has a Sharpe of 0.77 and a Calmar of 0.64, against the full book's 0.38 and 0.13.
- **F2:** The book's deepest fall was -0.56. It lasted 414 days, from w2 to w5. Shorts summed to -0.58 of it and longs to only -0.17, while the coins rose by a summed 0.58 over the same days. The book was short into rising coins.
- **F3:** The book's shorts pay the market's own rise. Their market part is -0.000638 a day, against a timing part of only +0.000235. Over the whole book, the market part is -0.000024 and timing is +0.000387 a day. That leaves a mean daily return of 0.00036, far below holding's 0.00118. Across 2132 SHORT trades the mean is -4.73 % after fees, against +8.42 % across 1856 LONG trades.
- **F4:** The forecast does not order the next 14 days' returns. The pooled slope has t = -0.30 over 1152 non-overlapping cases. The most negative forecast bucket, (-20, -10], was followed by a mean 14-day return of +3.4 % (n = 320). The most positive bucket, (10, 20], was followed by +1.1 %, with a median of -2.7 % (n = 272).
- **F5:** Within each 100-day trend state, the share runs the wrong way. The slope of the 14-day excess return on the forecast has t = -2.51 below the 100-day average and t = -2.02 above it (216 cases each). A longer stay above 50, compared within the same trend, is followed by weaker returns.
- **F6:** When the book was short with the close below its 100-day average, the coin still rose 0.0009 a day on average over 3711 bars. When it was long with the close above its 100-day average, the coin rose 0.0022 a day over 3669 bars. Being long only above the 100-day average had a Sharpe of 0.68, against the book's 0.38.
- **F7:** The loss is spread across the coins, but XRP is the worst. Its book returned -0.0011 a day while holding it returned +0.0013 a day. ZEC and XMR also earned 0.0012 to 0.0009 a day less than holding.

## Ideas
- `010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.d1_rsi-stretch-exhausts-within-trend` (from F5, F4): Comparing days on which a coin closes on the same side of its 100-day average price, the larger the share of the past 30 days that its 14-day RSI has spent above 50, the lower the coin's return over the next 14 days.
- `010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.d2_distance-above-100-day-average` (from F6, F1, F2, F3): The further a coin's close stands above its 100-day average price, the higher its return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-01_liquidation-flush-rebound
line: 7.d not profitable
backtest: 012-01_liquidation-flush-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a bar closes sharply lower on volume far above its own 30-day average volume and leaves a long lower wick below its close, price rises over the next 3 days, only after earlier such flush bars in the preceding 5 days. The more flush bars the coin has had over those 5 days, and the more extreme the volume burst and the longer the wick, the larger that rise.
Consequence: A trader would buy only into the second or later flush of a cascade and pass on the first flush, where the coin keeps falling, which removes about a third of the held bars that lose money and pay fees.
Why:
- F2: A lone flush gives no rebound and repeated flushes do: the 3-day excess return on grid flush bars is -0.0016 (t -0.33, n 329) with no flush in the prior 5 days, 0.0084 (t 1.88, n 352) after one, and 0.0210 (t 3.33, n 290) after two or more.
- F3: The book loses on the lone flush and gains on the repeated ones: the held daily gain is -0.0010 on 1029 bars with no prior flush in 5 days, against 0.0052 (n 1118), 0.0062 (n 704) and 0.0073 (n 302) after one, two and three or more.
- F1: The book earns a mean daily return of 0.000387, below the 0.0005 floor, against 0.00118 for holding the coins, with a deepest fall of -28.5% (Calmar 0.40), and it is in a position on only 18.0% of bars at a mean allocation of 0.84.
- F6: Fees take a large share of the gain: 0.000257 per bar against a gross gain of 0.000651. Trades are short (median 1 day, 2655 trades), and the 603 trades lasting 1.5 to 3.5 days lose -3.58% net on average.

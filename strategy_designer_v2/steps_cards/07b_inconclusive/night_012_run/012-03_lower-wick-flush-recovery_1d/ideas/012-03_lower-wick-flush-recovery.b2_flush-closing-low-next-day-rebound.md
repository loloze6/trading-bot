---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.b inconclusive
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply on a volume burst, the nearer the close sits to the bar's low, as a share of the bar's high-to-low range, the larger the price rise over the next 1 day.
Consequence: A flush that closes at its low has not yet been absorbed, and the snap-back comes the next day, so a trader buys the flushes that close weakest for a one-day rebound rather than those already showing a wick.
Why:
- F2: The plan's 3-day horizon falls where the effect turns over. Over 1 day the same slope is −0.073 with t −2.43 (n=226), the opposite of the idea. Over 5 and 10 days it is +0.008 (t 0.18) and −0.064 (t −1.21), so the positive 3-day reading is a crossing point, not a peak.
- F3: Over the next day, flush bars that close nearer their low rebound more. By quartile of close-near-low (1 − wick: 0.54, 0.74, 0.84, 0.94), the next-day excess return rises −0.013, −0.004, +0.010, +0.029 (about 41 bars each). Controlling for fall size and log volume ratio, that slope is +0.097 with t 2.78, while fall size has t −0.14.
- F4: The next-day rebound after a close near the low is broad across coins but uneven across years. It is positive in 5 of 6 coins (t 0.54 to 1.67; ZEC −0.35). By year it ranges from t −1.00 (2018) to t 4.54 (2022). The tested 3-day slope is also mixed by year, from t +1.59 (2018) to t −2.23 (2021).

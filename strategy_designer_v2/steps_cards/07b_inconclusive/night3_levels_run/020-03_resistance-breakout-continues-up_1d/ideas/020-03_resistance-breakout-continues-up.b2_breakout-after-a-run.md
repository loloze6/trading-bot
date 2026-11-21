---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, and the larger its 20-day return before the break and the more times the level held, the larger the rise.
Consequence: A break through a repeatedly held level after a strong run is a reason to buy for the following days, while a break after a flat or falling month is not.
Why:
- F4: The effect shows mostly when the coin was already rising before the break. Cases in the top quarter of the prior 20-day return (median +25 %) gain +1.72 % over 5 days (t 2.53, 369 cases), against −0.44 % in the bottom quarter. The same top quarter gives +1.71 % over 3 days (t 3.22) and +3.08 % over 10 days (t 2.72). Measured on the prior 10-day return, the top quarter gains +2.30 % (t 3.19).
- F5: Inside that rising half, the level's strength grades the move as the idea says: cases above the median of N × margin gain +1.91 % (t 2.74, 365 cases) against +0.51 % below it. Over all cases, the raw-value quintiles are not monotone (+0.19 %, −0.63 %, +1.15 %, +0.03 %, +0.84 %).
- F6: The prior-rise effect is not steady. Its overall Spearman correlation with the 5-day excess return is only 0.04. Only 54 % of windows have a positive mean in the rising half, against 46 % in the falling half. In 2022 both halves lose (−1.47 % and −1.51 %).
- F7: The idea is large enough to pay its costs: per case, the total move (+0.90 %) is 4.7 times the 0.19 % cost of a round trip, and the unusual move alone is 1.6 times it. The book beats holding on Sharpe (0.74, 0.19 above holding's) but fails on its falls (Calmar 0.49).

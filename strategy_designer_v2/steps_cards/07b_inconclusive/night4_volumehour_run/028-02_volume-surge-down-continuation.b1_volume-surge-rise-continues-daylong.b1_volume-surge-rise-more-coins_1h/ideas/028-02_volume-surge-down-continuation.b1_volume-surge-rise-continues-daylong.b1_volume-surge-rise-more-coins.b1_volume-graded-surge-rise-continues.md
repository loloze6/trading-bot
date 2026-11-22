---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
line: 7.b inconclusive
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's volume relative to its 30-day average, the larger the further rise.
Consequence: A trader would buy after a large hourly rise on heavily surging volume and hold for about a day, and would refuse to short such hours, with more conviction the heavier the volume.
Why:
- F1: The tested forecast does not single out surge hours. It is positive on 44–49 % of all bars and at least 2 on 11–14 % of bars for every coin, so most of its cases are ordinary up hours. Read once per 24-hour cell, those 17,245 cases have a mean unusual 24-hour move of −0.01 % (t −0.26), and even the top forecast quartile reaches only +0.12 % (t 1.35, 4,311 cases).
- F2: Taken on its own words, the situation shows the predicted effect. Recomputed from prices, hours rising at least 2.5 usual hourly moves on more than 3 times the 30-day mean volume are followed by an unusual 24-hour rise of +0.48 % (t 3.09, 1,910 cases). By volume ratio, the move is +0.23 % (t 1.15) under 1.5x, +0.18 % (t 1.07) at 1.5–3x, +0.36 % (t 2.03) at 3–6x and +0.68 % (t 2.37) above 6x.
- F3: Inside those high-volume up hours, the size of the rise does not grade the move, so the rise-times-volume product mixes a graded factor with an ungraded one. The 24-hour move is +0.53 % (t 2.92) for rises of 2.5–4 usual moves, +0.54 % (t 1.79) for 4–6 and +0.06 % (t 0.11) above 6. Across all up events, the correlation of log volume ratio with the move is only 0.022 (t 1.36, 3,975 cases).
- F4: The up-surge continuation is uneven across coins and years.
- F7: Against the cost, the tested measure's total move of +0.15 % per case is 0.8 times the 0.19 % cost of a trade. The true up surges of F2 (+0.48 % unusual) and the 2-hour continuation after the strongest down surges (−0.41 % to −1.06 %) are both larger than that cost.

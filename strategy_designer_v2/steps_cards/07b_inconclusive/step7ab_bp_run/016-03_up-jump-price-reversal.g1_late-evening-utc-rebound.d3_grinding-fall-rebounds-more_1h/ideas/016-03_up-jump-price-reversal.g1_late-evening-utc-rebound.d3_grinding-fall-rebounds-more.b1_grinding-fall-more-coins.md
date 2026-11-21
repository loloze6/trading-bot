---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days.
Consequence: A grinding daily decline is a better long for the next two days than an equally deep one made by a single violent hour.
Why:
- F1: The tested slope is on the side the idea predicts but well short of the bar. Its t is 0.91 on 8,579 grid cases, of which 4,191 have a positive forecast, and grind minus jump is +0.29 %. The effect is small: the unusual move is +0.08 % per case, a strength of 0.011 against the usual ~0.05 (findings F10). That is 0.4 times the 0.19 % round trip, a size that has never paid (findings F11).
- F3: The effect is mixed across coins and years. The slope t by coin runs from -0.85 (ETH) to 2.12 (XMR), with BTC 0.21, LTC 1.29, XRP -0.54 and ZEC 0.22. By year it is positive in 6 of 8 years but at or above 2 only in 2022 (2.05); 2024 is -1.31.
- F7: More data exists than the test used. It ran on 6 coins, while 13 more have hourly bars in folds A and D and partly in B and C.

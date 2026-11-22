---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin falls over its last day by much more than its usual 4-hour move over the past 30 days, on volume above its own 30-day norm, it rises over the next three days. The larger the fall and the heavier the volume behind it, the larger the rise.
Consequence: A heavy-volume one-day drop is a reason to buy for three days rather than to sell into it.
Why:
- F1: Large one-day falls on heavy volume are followed by a rebound. Score each fall by its 6-bar loss in usual moves times exp(its 6-bar volume z-score). The top quintile of that score shows a mean unusual 18-bar move of +2.00 % (t 7.2, 1092 independent cases, strength 0.21). The lower quintiles read -0.55 %, -0.35 %, -0.24 % and -0.10 %. The effect is positive in 18 of 19 coins and in 7 of 8 years; 2022 is the exception at -0.60 %, t -0.84.
- F2: In the cross of 6-bar direction, size and volume, the cell with the largest falls and the top third of volume gains +1.98 % over 18 bars (t 6.66, n 919). The largest falls on low volume gain only +0.83 % (t 1.70, n 268). The rebound grows with the volume behind the fall.

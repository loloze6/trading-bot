---
brief: 016_grind-versus-jump-moves
source-idea: 016-08_down-volume-burst-reversal
line: 7.b inconclusive
backtest: 016-08_down-volume-burst-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger the share of that period's volume traded in its few busiest hours, the more of the fall the coin wins back over the next 3 days.
Consequence: Down moves made with a burst of volume are forced selling that overshoots, so they partly reverse.
Why:
- F1: The tested measure is on the side the idea predicts but too small for this data. The top-half minus bottom-half excess 72-hour return is +0.0033 with Welch t 1.05 on 2,762 grid cases (1,381 per half). At this effect size, reaching t = 2 would take about 10,000 cases, roughly 3.6 times what the six default coins provide.
- F2: The effect is weak and graded only loosely. The rank correlation of forecast with excess 72-hour return is rho 0.028 (p 0.14, n 2,762). Across forecast quintiles the mean excess return is not monotone: -0.0075, +0.0017, -0.0049, +0.0004, +0.0027.

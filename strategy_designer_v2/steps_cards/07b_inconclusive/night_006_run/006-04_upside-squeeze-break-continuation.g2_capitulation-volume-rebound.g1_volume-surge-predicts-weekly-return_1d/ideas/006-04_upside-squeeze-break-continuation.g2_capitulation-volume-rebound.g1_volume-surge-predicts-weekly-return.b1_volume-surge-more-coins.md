---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin, the higher its 5-day average volume against its 30-day average, the higher its return over the next 7 days, whatever the direction of its last 5 days.
Consequence: A trader would lean long on coins whose recent volume runs above its monthly norm, and would not hold coins whose volume has dried up.
Why:
- F1: The tested measure lies on the side the idea predicts but just short of the bar: the 7-day slope is +0.000462 with t = 1.94 over 2443 independent cases, the top-minus-bottom tercile difference is +0.0075, and the 7-day quintile means of excess return run from -0.0018 and -0.0086 in the two lowest to +0.0085 and +0.0064 in the two highest. That spread is small against a 7-day excess-return standard deviation of 0.134, so the market's own moves largely drown it.
- F3: At 7 days the effect is concentrated in part of the data. XRP gives t = 2.90 and ZEC t = 1.15, against BTC at -0.06 and XMR at -1.22 (about 407 cases each). By year, 2024 gives t = 3.90, against 2018 at -0.89 and 2019 at -0.01 (about 300 cases each).

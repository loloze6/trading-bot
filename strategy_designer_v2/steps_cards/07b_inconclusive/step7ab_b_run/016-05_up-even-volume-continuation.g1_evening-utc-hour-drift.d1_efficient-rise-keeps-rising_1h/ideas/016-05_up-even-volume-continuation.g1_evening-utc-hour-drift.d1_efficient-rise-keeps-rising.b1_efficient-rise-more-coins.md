---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
line: 7.b inconclusive
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The more efficiently a coin has risen over its past 3 days (its 3-day rise large relative to the sum of its absolute hourly moves), the more it keeps rising over the next 3 days.
Consequence: A steady, efficient 3-day rise is a reason to be long for the following days, larger the steadier the rise, with a move several times a round trip.
Why:
- F1: The tested measure is on the predicted side but small and mixed. Its mean is +0.27 % (t 1.41, 2916 cases). By coin it ranges from -0.29 % (LTC, t -0.62) to +0.84 % (XRP, t 1.31). By year it swings from -1.14 % (2019, t -2.01) to +1.20 % (2020, t 2.15). The size is an unusual move of -0.13 % per case, a strength of -0.016, against a cost of 0.19 %.

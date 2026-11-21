---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the smaller the share of that rise that came from its few biggest hourly gains (a grind of many small hourly steps), the more the coin keeps rising over the next 3 days.
Consequence: A trader would go long into grinding 3-day rises and size the position by how evenly the rise was spread across hours, instead of shorting jump-made rises that still drift up.
Why:
- F1: The tested effect points the way the idea predicts but falls short of the bar. On the plan's non-overlapping 72-bar grid of rising cases, the forecast's coefficient beyond rise size is +0.000341 with t = 1.52 over 2,865 cases. The raw grind measure gives +0.0214 with t = 1.76 over the same cases.
- F3: The effect is mixed across coins and years. The grind t is 2.74 for BTC and 2.08 for LTC, but -0.21 for ETH, -0.39 for ZEC and 0.35 for XMR, each on about 460 to 500 cases. By year it is 1.95 in 2019 and 2.00 in 2024, but -0.64 in 2018 and -0.46 in 2025.

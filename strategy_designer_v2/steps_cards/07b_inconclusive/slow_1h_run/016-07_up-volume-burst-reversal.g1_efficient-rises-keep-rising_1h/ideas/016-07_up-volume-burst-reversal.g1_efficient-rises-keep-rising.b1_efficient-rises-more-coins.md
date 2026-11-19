---
brief: 016_grind-versus-jump-moves
source-idea: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
line: 7.b inconclusive
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 2 to 3 days, the more of its hourly movement over that period went in the direction of the rise (net move relative to the sum of absolute hourly moves), the more it rises over the next 3 days.
Consequence: A smooth, steady multi-day rise is a reason to hold or join it for about three days, and a choppy rise of the same size is a reason to stay out.
Why:
- F3: The test's main measure is on the predicted side but short of the bar. The forecast slope is +0.000365 with t 1.19 on 2254 cases. The forecast-weighted mean excess is +0.0038. The lowest forecast quintile alone is negative (-0.0032), and the other four are flat between +0.0001 and +0.0058.
- F5: The effect is spread thinly rather than concentrated. The raw-ratio slope is positive in all 6 coins (t from 0.01 for ETH to 2.39 for LTC) and in all 8 years (t from 0.00 in 2022 to 2.24 in 2024). The forecast slope is positive in 5 of 6 coins and 7 of 8 years, with none reaching t 2. Each subset of 350 to 390 cases is too small to show it alone.

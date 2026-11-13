---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the death-cross state, a coin whose recent daily volatility is high tends to rise rather than keep falling. The downward drift appears only, if at all, when volatility is calm.
Consequence: A trader should refuse death-cross shorts in volatile conditions and keep any such short to calm markets.
Why:
- F7: Losses grow with volatility: gross per active bar is +0.000017 in the calm tercile, -0.000879 in the mid tercile and -0.001271 in the volatile tercile.
- F5: The losses depend on the market regime. The short earned in the bear years 2018 (+2.62 gross, coin -0.0035/day, 76% active) and 2022 (+0.93, coin -0.0018/day, 93% active). It lost heavily in the rising years 2020 (-5.35, coin +0.0042/day), 2024 (-2.96) and 2023 (-1.72).

---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the short average is below the long one, the coin keeps falling only when its own return over the prior weeks, known at the bar's close, is already negative. This is the case in broad bear phases.
Consequence: A trader should short a death cross only when the coin's recent trend is already down, and refuse it when the coin has been rising since the cross.
Why:
- F5: The losses depend on the market regime. The short earned in the bear years 2018 (+2.62 gross, coin -0.0035/day, 76% active) and 2022 (+0.93, coin -0.0018/day, 93% active). It lost heavily in the rising years 2020 (-5.35, coin +0.0042/day), 2024 (-2.96) and 2023 (-1.72).
- F6: The short pays only when the coin is already falling over the current 20 days and loses when it is rising: gross is +0.006132 a bar in the falling-momentum tercile against -0.006930 in the rising tercile. This split is contemporaneous with the bar's own return, so it describes where the losses fall, not a forecast.
- F2: The coin rises while the book is short: the mean daily coin return on short bars is +0.000777 against +0.001287 on all bars, and the 10-bar forward return in the short state is 0.0128 against 0.0135 overall, so the death-cross state carries almost no downward drift relative to holding.

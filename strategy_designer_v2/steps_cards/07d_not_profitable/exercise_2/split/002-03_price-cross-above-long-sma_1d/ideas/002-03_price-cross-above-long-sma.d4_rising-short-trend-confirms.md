---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin is above its 200-day SMA and its 20-day trend is rising, it keeps rising over the next 20 bars by more than its average 20-bar return.
Consequence: Require a rising 20-day trend before holding the long, because the book's above-SMA position lags holding mainly when the shorter trend is falling.
Why:
- F9: The book lags holding when the 20-day trend is falling, earning -3.0, +1.6 and -0.7 bp a day in calm, mid and volatile falling markets against holding's -11.3, +7.7 and +13.7; it beats holding only in volatile rising markets, at 46.8 bp against 35.6.
- F10: By year, the book gives up most of holding's gain in 2023 (-2.0 bp a day against +15.0, while active 61% of bars) and in 2020 (19.4 against 42.3), while it saves in 2018 (-6.9 against -34.8) and 2022 (-3.6 against -18.0).

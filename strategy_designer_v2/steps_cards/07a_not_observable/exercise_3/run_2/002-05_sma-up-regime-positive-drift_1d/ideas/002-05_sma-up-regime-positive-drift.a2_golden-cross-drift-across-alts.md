---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A and D
---
Idea: On a coin's daily bars, while its 50-day average sits above its 200-day average, its return over the next 1 day is higher than its average, and the further the 50-day average stands above the 200-day one, the larger that next-day rise.
Consequence: If confirmed, a trader has a reason to hold a coin long in proportion to how far its 50-day average leads its 200-day one; if rejected, a reason to refuse golden-cross longs.
Why:
- F1: The test ran on a single coin (BTCUSD) and a single window (w1) of 120 daily bars, all in 2022. Only 13 bars had the 50-day SMA above the 200-day SMA (forecast > 0) against 107 out of stretch, and there was 1 up-cross stretch. The plan asked for at least 100 in-stretch bars and 3 stretches.
- F2: The situation is rare in this sample because 2022 was a bear year. The spread was positive only in the window's first 20-bar block (mean +13.7, 65 % of bars in stretch). It was negative in every later block (block means -49.0, -82.2, -88.5, -71.3, -61.4), and there was 1 down cross and no new up cross.
- F4: The outcome varies a lot from day to day. The next-bar return had a standard deviation of 3.32 % (2.33 % in stretch), against an in-minus-out mean difference of -0.69 %/day (t -0.95). At that noise, a 0.2 %/day edge needs about 2,205 bars per group to reach t = 2, and a 0.1 %/day edge needs about 8,819. So far more coins and years than one window are needed.
- F5: Golden-cross stretches last months and come about once a cycle per coin, which makes the situation slow compared with 120-bar windows. The plan's minimum of 3 stretches and 100 in-stretch bars can only be reached by pooling many coin-windows across bull and bear years.

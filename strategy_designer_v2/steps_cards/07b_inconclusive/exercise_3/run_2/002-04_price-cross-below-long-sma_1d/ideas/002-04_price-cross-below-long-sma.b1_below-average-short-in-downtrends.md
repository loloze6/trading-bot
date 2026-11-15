---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is below its 200-day moving average, the price keeps falling beyond its usual drift over the following days, only while that long average is itself falling, and the faster the average falls the further the price drops.
Consequence: A trader would short coins under their long average only in a falling-average (bear) market and refuse the short while the long average is still rising.
Why:
- F2: The effect flips sign by year, so the pooled mean cancels: the 10-bar excess fall is positive in the bear years 2018 (+0.0365, t 2.18, n 133), 2019 (+0.0165, t 1.85, n 140) and 2022 (+0.0232, t 2.48, n 195), and negative in the bull years 2020 (-0.0257, t -1.72, n 87), 2021 (-0.0683, t -2.78, n 68) and 2024 (-0.0157, t -1.59, n 109).
- F4: Being below the average carries no information on its own: flat blocks above the SMA200 show a 10-bar excess return of +0.0028 (t 0.42, n 726), about the same size as the short side's +0.0020, and no coin is significant (t from -0.35 for XRP to 0.57 for XMR).
- F5: The market's own rise sinks the book. The gross short gain before the mean is removed is -0.0054 per 10-bar block (t -2.53, n 931) and stays negative at every horizon (t -2.1 to -2.6), while the excess part is about zero (F1). The book's Sharpe of -0.43 comes from shorting coins that drift up, not from bad timing.

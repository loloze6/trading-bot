---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin closes above its long moving average, the nearer its close sits to the top of its recent range and the stronger its recent rise, the larger its return over the following days to two weeks. The effect fades by about a month.
Consequence: Hold momentum longs inside an uptrend for days to a couple of weeks, not a month, and size them by how close price is to its recent high.
Why:
- F1: The pooled 336-bar slope's t of 2.18 (576 cases) rests on a few large gains. Dropping the 3, 5 or 10 largest excess returns cuts it to t 1.35, 0.74 and 0.68. Winsorising at 2.5/97.5 % gives t 1.29, and the rank correlation of forecast with excess return is −0.0009 (p 0.98).
- F2: In the top forecast bin (above 10, 174 cases) the mean excess return is +0.048 but the median is −0.025, and only 45 % of cases are positive, against 47 % at a zero forecast. The mean is lifted by right tails, mostly in ZEC (mean +0.120, median −0.071) and XRP (mean +0.077, median −0.028).
- F3: The effect is mixed across coins and years. The per-coin slope t ranges from −0.16 (ETH) and −0.14 (LTC) to +1.70 (ZEC). The per-year t swings from +2.26 (2019) and +2.40 (2021) to −2.17 (2023).

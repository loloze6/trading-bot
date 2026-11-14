---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits only slightly above its 200-day average, the next 20 bars more often end lower than the coin's usual drift. This holds most often in the weeks right after an upward cross.
Consequence: A trader should not buy a coin merely because it has edged above its long average.
Why:
- F2: Bars just above the 200-day SMA (forecast 0–5, n=1,909) had a mean next-20-bar return of −0.25%, a median of −1.65% and a 38.8% hit rate. Flat bars (n=7,297) had +2.60% mean and 43.0% hit. The 15–20 forecast bucket had +6.30% mean but a −0.11% median and 40.0% hit, so the edge from a larger distance is in the mean only.
- F6: The cross events themselves show little continuation. After an upward cross (n=278), the next 5 bars returned +0.05% and the next 20 returned +2.47% (median +1.57%, hit 44.6%). After a downward cross (n=280), the next 5 bars returned +0.92%, a short-term bounce, while the next 20 had a +1.09% mean but a −1.30% median and a 39.6% hit rate.
- F1: The book's whole profit comes from trades held longer than 30 days. Those 515 trades averaged +33.8% net, won 69.7% of the time and summed to +17,412%, against a total book P&L of +9,206%. Every shorter bucket lost on average: 241 trades of 1 day or less averaged −6.26% with a 1.2% win rate, 332 trades of 1–3 days averaged −6.54% (4.5% win rate), 526 trades of 3–10 days averaged −5.77% and 611 trades of 10–30 days averaged −2.44%. These short trades are 1,710 of the 2,228 trades, all of them long.

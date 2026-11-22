---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move is small next to its 30-day high-low range, the closer its close sits to the top of that range, the further it falls over the next five days.
Consequence: A trader would fade a flat coin pressing the top of its month's range, and would not buy one at the bottom on the same reasoning.
Why:
- F5: The brief's range reversion shows only at the top of a flat range, on non-overlapping 5-day returns. With net move under a quarter of the 30-day range, coins near the top fell −2.36 % excess (t −2.40, 105 cases). Coins near the bottom did not rise (−0.41 %, t −0.56, 169 cases).

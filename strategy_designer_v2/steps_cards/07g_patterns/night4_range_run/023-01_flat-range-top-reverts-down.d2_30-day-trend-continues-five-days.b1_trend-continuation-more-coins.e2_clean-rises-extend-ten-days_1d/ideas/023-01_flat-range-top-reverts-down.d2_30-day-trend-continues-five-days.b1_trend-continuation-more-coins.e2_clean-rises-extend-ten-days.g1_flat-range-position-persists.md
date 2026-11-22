---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move covers only a small share of its 30-day high-low range, the higher its close sits within that range, the more it rises beyond its normal drift over the next 10 days. The lower its close sits, the more it falls short of that drift.
Consequence: A trader would not fade the edges of a flat month, and would avoid holding a flat coin that sits low in its range for the next 10 days.
Why:
- F1: In flat coins, where the 30-day net move covers less than half the 30-day high-low range, prices kept going the same way instead of reverting. Sorted by where the close sits in the 30-day range (1,595 non-overlapping 10-day cases), the 10-day excess over normal drift rose from the bottom up:
- F2: The coin's whole spread of 30-day moves points the same way. Sorted by the signed 30-day net-move-to-range ratio (268 cases per decile), the middle deciles 2 to 5 lost −2.2 %, −3.1 %, −1.0 % and −2.1 % over 10 days (t −2.5, −3.5, −1.2, −2.2). The top three deciles gained +1.7 %, +2.9 % and +3.0 % (top t 2.3). The overall rank correlation was +0.04.

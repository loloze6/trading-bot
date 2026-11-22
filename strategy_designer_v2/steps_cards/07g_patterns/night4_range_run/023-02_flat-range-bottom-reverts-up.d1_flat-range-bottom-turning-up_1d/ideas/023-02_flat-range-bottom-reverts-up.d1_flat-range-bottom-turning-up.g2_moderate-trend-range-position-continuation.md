---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move is moderate against its 30-day high-low range, the higher its close sits in that range, the more it rises over the next 5 days.
Consequence: In a coin with a moderate trend, a trader buys strength near the top of the monthly range instead of fading it.
Why:
- F5: The brief's reversion is absent in flat coins (30-day net move at most 0.3 of the 30-day range). The slope of the drift-removed 5-day return on the close's place in the range is −0.085 (t −0.58, n 835). Flat coins in the lowest fifth of the range gain only +0.71 % over 5 days (t 1.03), and those in the highest fifth lose −1.50 % (t −1.17).
- F6: In coins with a moderate trend, the place in the 30-day range points the other way, toward continuation.

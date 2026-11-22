---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day rise when that rise spans much of its 30-day high-low range, the higher its return over the next five days.
Consequence: A trader would follow a coin's strong 30-day rise on the long side, rather than bet on 30-day falls continuing.
Why:
- F1: The book's whole result rests on its long side. Long bars gained a mean +0.32 % per bar (t 6.09, 7922 bars). Short bars lost a mean −0.04 % (t −1.20, 7713 bars). The signed next-day excess move was +0.21 % after rises (t 3.14) and only +0.07 % after falls (t 1.09).
- F6: Away from flat ranges, position in the 30-day range continued over 5 days rather than reverting. In the middle band of net move, the top of the range was followed by +2.23 % (t 2.10, 157 cases) and the bottom by −3.09 % (t −3.86, 183 cases). In trending coins the top was followed by +1.87 % (t 2.44, 706 cases).

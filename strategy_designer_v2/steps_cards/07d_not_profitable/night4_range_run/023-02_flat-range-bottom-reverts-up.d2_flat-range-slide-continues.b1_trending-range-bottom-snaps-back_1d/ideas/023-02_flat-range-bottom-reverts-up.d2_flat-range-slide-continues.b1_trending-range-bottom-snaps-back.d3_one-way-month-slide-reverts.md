---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose close sits below the middle of its 30-day high-low range after a deep 10-day fall, the larger its 30-day net move relative to that range, the more it rises over the next 5 days.
Consequence: The more one-way a coin's month has been, the stronger the case for buying its deep slide rather than chasing the breakdown.
Why:
- F5: Deep falls rebound mainly when the month is strongly one-way: deep falls with a net-move-to-range ratio above the median give +5.19 % excess (n 71), against +0.32 % (n 70) below it; shallow falls lose -3.20 % and -2.81 % either way.
- F2: The idea's effect lives only in its deepest falls: on the 5-day grid, active cells in the two lower forecast quartiles (mean forecast 2.7 and 6.9, 10-day fall -3.2 % and -9.3 %, n 283) have excess returns of -1.78 % and -2.15 %, while the two upper quartiles (forecast 12.6 and 19.4, fall -15.3 % and -22.9 %, n 282) have +2.28 % and +1.99 %; cells with forecast of at least 10 average +2.77 % excess (t 2.52, n 141).

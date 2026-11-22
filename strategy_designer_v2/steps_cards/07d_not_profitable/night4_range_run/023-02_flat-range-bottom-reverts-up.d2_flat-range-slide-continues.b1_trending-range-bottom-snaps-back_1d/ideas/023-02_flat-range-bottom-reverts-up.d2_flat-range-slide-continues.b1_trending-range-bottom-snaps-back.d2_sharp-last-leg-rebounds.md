---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 3 days, the more it rises over the next 5 days.
Consequence: A trending coin's sharp final drop below its month's mid-range is the bar to buy, while a slow drift lower is not.
Why:
- F6: A sharp last leg carries the rebound: active cells whose 3-day return is in the lowest tercile (-11.4 %) have +2.14 % excess, against -1.37 % and -0.93 % in the other two (n 92 each); the same holds for the lowest range position (-0.43: +1.54 %, against -0.21: -1.71 %) and the highest 20-day volatility tercile (+1.84 %, against -0.47 % and -0.80 %).
- F2: The idea's effect lives only in its deepest falls: on the 5-day grid, active cells in the two lower forecast quartiles (mean forecast 2.7 and 6.9, 10-day fall -3.2 % and -9.3 %, n 283) have excess returns of -1.78 % and -2.15 %, while the two upper quartiles (forecast 12.6 and 19.4, fall -15.3 % and -22.9 %, n 282) have +2.28 % and +1.99 %; cells with forecast of at least 10 average +2.77 % excess (t 2.52, n 141).
- F1: The book's falls and its edge over holding are what failed: its mean daily return is 0.0118 % against holding's 0.118 %, its market part is 0.0171 % a day and its timing is -0.0012 % a day, so none of its gain comes from timing, and its chained yearly return of 2.0 % sits against a deepest fall of -41.8 % (Calmar 0.048), running from w14 to w16, with w14 alone at -28.5 % (holding -52.2 %) and w2 at -17.2 % (holding -45.9 %).

---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
line: 7.d not profitable
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range and whose close sits below the middle of that range, the larger its fall over the past 10 days measured in units of its usual 10-day move over the past 60 days, the more it rises over the next 5 days.
Consequence: Only a slide that is extreme for the coin's own volatility is a reversion long; a mild slide below the range middle is a long to refuse.
Why:
- F2: The idea's effect lives only in its deepest falls: on the 5-day grid, active cells in the two lower forecast quartiles (mean forecast 2.7 and 6.9, 10-day fall -3.2 % and -9.3 %, n 283) have excess returns of -1.78 % and -2.15 %, while the two upper quartiles (forecast 12.6 and 19.4, fall -15.3 % and -22.9 %, n 282) have +2.28 % and +1.99 %; cells with forecast of at least 10 average +2.77 % excess (t 2.52, n 141).
- F3: Per bar, the book loses where the forecast is moderate: bars with forecast 5-10 sum to -1.17 in bar gains (mean -0.17 %, n 707) and bars with forecast 10-15 sum to -0.19, while bars with forecast 15-20 earn +4.17 (mean +0.48 %, n 877).
- F4: Measured against the coin's own volatility, the 10-day fall grades the rebound cleanly: across quartiles of the fall over its 60-day usual 10-day move (z -1.87, -1.01, -0.58, -0.24; n 69 each), the excess 5-day returns are +3.31 %, +1.58 %, -1.87 % and -3.24 %.
- F7: The step-5 size shows a total move per case of +0.23 % against a trade cost of 0.19 % (1.2 times), with an unusual move of -0.37 % (strength -0.030), because the shallow-fall cases cancel the deep ones: the effect is large only in the steep, volatility-scaled falls of F2 and F4.
- F1: The book's falls and its edge over holding are what failed: its mean daily return is 0.0118 % against holding's 0.118 %, its market part is 0.0171 % a day and its timing is -0.0012 % a day, so none of its gain comes from timing, and its chained yearly return of 2.0 % sits against a deepest fall of -41.8 % (Calmar 0.048), running from w14 to w16, with w14 alone at -28.5 % (holding -52.2 %) and w2 at -17.2 % (holding -45.9 %).

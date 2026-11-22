---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range, the larger its 10-day rise, the more it rises over the next 5 days, and the larger its 10-day fall, the more it falls.
Consequence: In a flat coin, a 10-day push toward an edge of the range is something to follow rather than to fade.
Why:
- F2: In flat coins (net move under half the range), the 10-day return continues rather than reverts, against the brief. The slope of the 5-day excess return on the 10-day return z is +0.101 with t 3.33 over 1442 cases. The bottom 10-day quintile gives -1.14 % (t -2.05), the second -1.23 % (t -2.52) and the top +1.73 % (t 2.27). In trending coins the same slope is 0.011 (t 0.39, 1113 cases).
- F3: The flat-coin continuation is positive in all six coins (t from 0.54 in XMR to 2.02 in ETH) but not stable over time. Its slope is +0.258 (t 3.08) in 2018–2021, then -0.057 in 2023, +0.036 in 2024 and -0.213 (t -2.29) in 2025.
- F4: Flat coins closing in the bottom fifth of their 30-day range keep falling: their 5-day excess return is -1.81 % (t -2.57, 197 cases). The brief's reversion from the range bottom does not appear.

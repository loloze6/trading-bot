---
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3785 USD
---
## Findings
- **F1:** In trending coins (30-day net move at least half the 30-day high-low range), the size of the 10-day move in either direction predicts a higher 5-day return. Pooled over the coins, the slope of the 5-day excess return (z) on |10-day return z| is +0.187 with t 5.03 over 1113 non-overlapping cases. It is positive in all six coins, with t 4.22 in ZEC, 2.38 in ETH and 2.31 in XRP. Both tails rise: the bottom quintile of the 10-day return gives +1.71 % excess (t 2.01, 234 cases) and the top quintile +1.46 % (t 1.90, 301 cases), while the middle quintiles are near zero or negative.
- **F2:** In flat coins (net move under half the range), the 10-day return continues rather than reverts, against the brief. The slope of the 5-day excess return on the 10-day return z is +0.101 with t 3.33 over 1442 cases. The bottom 10-day quintile gives -1.14 % (t -2.05), the second -1.23 % (t -2.52) and the top +1.73 % (t 2.27). In trending coins the same slope is 0.011 (t 0.39, 1113 cases).
- **F3:** The flat-coin continuation is positive in all six coins (t from 0.54 in XMR to 2.02 in ETH) but not stable over time. Its slope is +0.258 (t 3.08) in 2018–2021, then -0.057 in 2023, +0.036 in 2024 and -0.213 (t -2.29) in 2025.
- **F4:** Flat coins closing in the bottom fifth of their 30-day range keep falling: their 5-day excess return is -1.81 % (t -2.57, 197 cases). The brief's reversion from the range bottom does not appear.
- **F5:** The tested idea's graded slope (t 3.79) rides on the coins' drift, not on a reversion. Its unusual move is -0.37 % per case (-0.030 of a usual 10.60 % move, 751 cases), and the total move of +0.23 % is only 1.2 times the 0.19 % cost of a trade.
- **F6:** The tested book earns little and does not grade with its forecast.
- **F7:** Saturday's daily coin return averages +0.45 % (t 3.04, 414 days, coins averaged). It is positive in all six coins (t above 2 in five of them) and above the other days in 7 of 8 years. It is a calendar condition, not a graded situation, so no idea is written from it.

## Ideas
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back.g1_trending-big-move-lifts` (from F1, F5): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 10-day move in either direction, the more it rises over the next 5 days.
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back.g2_flat-range-push-continues` (from F2, F3, F4): In a coin whose 30-day net move has been small relative to its 30-day high-low range, the larger its 10-day rise, the more it rises over the next 5 days, and the larger its 10-day fall, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

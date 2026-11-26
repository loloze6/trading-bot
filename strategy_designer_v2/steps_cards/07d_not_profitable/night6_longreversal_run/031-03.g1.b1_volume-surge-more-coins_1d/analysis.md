---
line: 7.d confirmed, not profitable
backtest: 031-03.g1.b1_volume-surge-more-coins_1d
idea tested: 031-03.g1.b1_volume-surge-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5922 USD
---
## Findings
- **F1:** The book's falls are what fail it: unchanged and before fees, the book has Sharpe 0.66, a deepest fall of −52.6 % and Calmar 0.30, against holding's Sharpe 0.62, so it barely beats holding. Most of the fall comes in w13 to w16 (2018 to 2020), where the book lost −0.17, −0.22 and −0.18 per window (summed daily returns). Over the same windows, holding gained +0.11 in w15 and +0.63 in w16.
- **F2:** The losing part of the book is the side that bets against the coin's own 14-day move. By bar gain (position × next-bar return), the book's four positions earn:
- **F3:** The idea's signal carries the effect, not the 14-day return alone, on the 14-day grid of excess returns:
- **F4:** Trading the signal only when its side agrees with the sign of the 14-day return raises the grid directional excess to +2.59 % per case (t 4.16, 1450 cases), against +1.85 % (t 3.49, 1836 cases) for all cases.
- **F5:** That book, before fees, has:
- **F6:** Size against cost: the tested idea's unusual move per case is +0.66 % (t 1.02) against a 0.22 % trade cost, a strength of only 0.026. The agreeing cases move about 2.6 % in excess per 14 days, which covers the cost many times.
- **F7:** Two other ways of trading it do less:
- **F8:** Long only, the book reaches Sharpe 0.96 and Calmar 0.75 before fees, below the agreeing book. Among the four positions, long with a 14-day rise carries the most gain per bar (+0.00245).

## Ideas
- `031-03.g1.b1.d1_volume-surge-with-price-move` (from F1, F2, F3, F4, F5, F6): The more a coin's mean daily volume over the last 14 days has risen above its mean daily volume over the last 30 days, the more its price rises over the next 14 days, while its own 14-day return is up. The more that volume has fallen below its 30-day mean, the more its price falls over the next 14 days, while its 14-day return is down.
- `031-03.g1.b1.d2_rising-volume-rally-continues` (from F2, F3, F7, F8): The more a coin's mean daily volume over the last 14 days has risen above its mean daily volume over the last 30 days, the more its price rises over the next 14 days, while its own 14-day return is up.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

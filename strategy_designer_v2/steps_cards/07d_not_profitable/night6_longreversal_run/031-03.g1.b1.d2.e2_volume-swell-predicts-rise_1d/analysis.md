---
line: 7.d confirmed, not profitable
backtest: 031-03.g1.b1.d2.e2_volume-swell-predicts-rise_1d
idea tested: 031-03.g1.b1.d2.e2_volume-swell-predicts-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4712 USD
---
## Findings
- **F1:** The book's loss is in its short side. Short trades lost 3.83 % gross and 3.93 % net on average over 6427 trades, while long trades gained 6.40 % gross over 5462 trades. Rebuilt on the book's own daily returns, the short-only part has a Sharpe of −0.28, a yearly return of −8.3 % and a deepest fall of −64 %, and the long-only part has a Sharpe of 0.91, a yearly return of +20.8 % and a Calmar of 0.67. The full book has a Sharpe of 0.57 and a Calmar of 0.24, and holding the coins has a Sharpe of 0.61.
- **F2:** The short side's unusual move is real but its total move does not pay. On the 14-day grid, short signals have an unusual move of −1.59 % (t −3.04, 1303 cases), but the coins' positive drift leaves a total move of −0.91 % per case in the short's direction. Long signals have an unusual move of +1.81 % and a total move of +4.32 % per case, against a trade cost of 0.22 %.
- **F3:** The deepest fall (−53 %, from window 14 to window 16, 220 days) came while the coins rose: holding summed +0.59 over the fall. Shorts carried −4.28 of the book's summed daily returns in it, against −0.86 for longs. The book's falls are short positions held through rising markets.
- **F4:** The long signal works when the coin is above its 50-day mean.
- **F5:** Removing the losing side fixes each measure that failed.
- **F6:** Long signals pay only when the coin's 14-day return is positive: +3.32 % unusual move (t 2.54, 602 cases) against −0.20 % when it is negative (439 cases). A long-only book on these days has a Sharpe of 1.08 and a Calmar of 1.18. That condition was not measured alone in this exploration.

## Ideas
- `031-03.g1.b1.d2.e2.d1_volume-swell-long-only` (from F1, F2, F3, F5): The more a coin's mean daily volume over the last 14 days sits above its mean daily volume over the last 30 days, the more its price rises over the next 14 days, on the long side only: the coin's swell is a reason to be long, and its drying up is no reason to be short.
- `031-03.g1.b1.d2.e2.d2_volume-swell-in-uptrend` (from F3, F4, F5, F6): The more a coin's mean daily volume over the last 14 days sits above its mean daily volume over the last 30 days, the more its price rises over the next 14 days, only while its close sits above its mean close of the last 50 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

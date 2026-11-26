---
line: 7.g patterns
backtest: 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d
idea tested: 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3964 USD
---
## Findings
- **F1:** The day after a coin's largest one-day falls, it rebounds more than its normal drift, and the rebound shrinks as the fall gets smaller. Bottom decile of the day's return over 30-day volatility: +0.55 % next day (t 2.06, 518 days, 1401 cases). Second decile: +0.29 % (t 1.71). Middle and upper deciles: between −0.23 % and +0.00 %. Spearman rank correlation between the size of the fall and the next day's unusual return, over all down days: −0.073 (p 1e-9, n 6889).
- **F2:** The rebound after a large fall grows with the coin's volatility level. Bottom fifth of one-day moves, by the coin's own 30-day volatility tercile: low +0.07 % (t 0.37, 480 days), middle +0.32 % (t 1.31), high +0.87 % (t 2.56, 460 days). That high-volatility move is 4.6 times the 0.19 % cost of a trade.
- **F3:** The rebound after a large fall is a one-day effect. On non-overlapping 3-day returns, the bottom fifth of one-day moves earns +0.51 % (t 0.99, 338 days), which cannot be told from 0. By coin it is positive in all six, from BTC +0.18 % (t 0.99) to XMR +0.73 % (t 3.43).
- **F4:** The tested Saturday effect is carried by the largest 20-day gains, not by the convex sizing. On Saturdays, quintiles of the 20-day return over volatility give an unusual return of −0.51 % (t −1.45), +0.19 %, +0.30 %, +0.25 % and +1.15 % (t 2.85, 381 cases). Saturdays after a 20-day gain earn +0.63 % (t 2.92, 257 days); after a 20-day loss, −0.08 % (t −0.41).
- **F5:** Outside the Saturday, the 20-day gain also lines up with the next day on Fridays. The Spearman rank correlation of the 20-day return with the next day's unusual return is +0.063 (p 0.005, 1999 cases) when the coming day is Friday. On other weekdays it runs from −0.050 to +0.037. This is one of seven weekdays scanned.
- **F6:** Distance from the 365-day low showed nothing. The few measurable cases (about 245) gave unusual next-day returns between −1.01 % and −0.23 % per quintile, all with |t| < 1.6. The brief's yearly-low question finds no measurable pattern in these bars.

## Ideas
- `031-01.g1.g2.d2.g1_volatile-one-day-fall-rebound` (from F1, F2, F3): The larger a coin's one-day fall, measured against its usual daily move over the past 30 days, the more it rises over the next day. The rebound is larger the more volatile the coin has been over the past 30 days.
- `031-01.g1.g2.d2.g2_monthly-gain-into-weekend` (from F4, F5): The higher a coin's 20-day return, measured against its usual 20-day moves, the more it rises over the next day when that day is a Friday or a Saturday (UTC).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

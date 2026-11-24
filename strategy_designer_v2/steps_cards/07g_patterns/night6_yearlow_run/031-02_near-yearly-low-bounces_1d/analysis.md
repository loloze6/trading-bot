---
line: 7.g patterns
backtest: 031-02_near-yearly-low-bounces_1d
idea tested: 031-02_near-yearly-low-bounces
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5489 USD
---
## Findings
- **F1:** Before a Saturday, a coin's 5-day return grades its Saturday return in the same direction: across 2014 coin-Saturdays the slope of the Saturday return on the prior 5-day return is +0.0896 (t 11.40, cases on the same Saturday not pooled across coins, so this t is optimistic). By tercile of the prior 5-day return, the Saturday mean is −0.38 % in the lowest (t −2.63, 672 cases), +0.48 % in the middle (t 4.95, 670) and +1.07 % in the highest (t 5.43, 672).
- **F2:** Saturday is the strongest day for the coins: the mean over the coins of their daily return is +0.47 % on Saturdays (t 3.14, 414 days), against −0.18 % to +0.32 % on the other weekdays (all |t| < 1.8). Saturday beat the other days in 7 of 8 years (not in 2023) and in all 6 coins (Welch t from 0.34 for BTC to 2.67 for LTC).
- **F3:** The book's small gain comes mostly from weekends and not from nearness to the low: Saturdays carry 71 % of the sum of its daily returns, Fridays 41 % and Sundays 26 %, while Thursdays take away 43 %. Over the whole period the book makes +2.4 % a year with a Sharpe of 0.26, against holding's 0.58.
- **F4:** Nearness to the yearly low does not grade the excess return at any horizon: the slope on log(1 + distance) has t −0.41 at 5 days (3326 cases), −0.43 at 10 days (1646 cases) and −0.91 at 20 days (806 cases). The five fifths of the distance give 20-day excess returns that are not monotonic: −1.7 %, −0.3 %, +3.9 %, +0.8 % and −2.7 %, all with |t| < 1.3.
- **F5:** The first close at a new 365-day low (events at least 20 days apart, 58 events on 41 days) shows no edge either way. Its 20-day excess return is +0.41 % (day-clustered t 0.08) and its 5-day excess return is −1.96 % (t −0.82). Deeper breaks show only a weak tendency to do worse over 20 days (slope on depth t −1.79), which cannot be told from chance.

## Ideas
- `031-02.g1_weekend-continues-the-week-s-move` (from F1, F2, F3): On the day after a Friday close, a coin keeps moving in the direction of its 5-day return: the larger its 5-day rise at Friday's close, the more it rises over the next day, and the larger its 5-day fall, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4173 USD
---
## Findings
- **F1:** Over the next 48 hours, a coin's past 5-day return carries on most strongly from Friday and Saturday 00:00. Regressing the 48-hour excess return on the 5-day move (in units of its std) gives a slope of +0.0052 per std with t 4.5 (n 2301) from Saturday starts and +0.0048 with t 3.8 (n 2293) from Friday starts, against −0.0032 (t −2.0) from Monday starts. Seven start days were tested and t 4.5 still clears that.
- **F2:** Sorted into quintiles by the previous week's (Mon→Sat) move, the next weekend's return rises roughly monotonically: −0.04 % (t −0.1), +0.26 %, +0.44 %, +0.76 % (t 2.8), +0.63 % (t 1.9), about 448 weekends each. The spread of about 0.7 % between the extreme quintiles is several times the 0.19 % cost of a trade.
- **F3:** The weekend momentum of F1 is not even across coins or years. By coin the Saturday-start slope has t 4.2 for XRP and 3.3 for ETH, but only 0.6–1.1 for BTC, LTC, XMR and ZEC. By year it is positive in 2018 (t 3.6), 2019 (t 3.0) and 2024 (t 4.3), and negative in 2020 (t −1.0) and 2023 (t −1.8).
- **F4:** The brief's weekend reversal is absent. The weekend move has a correlation of −0.007 (slope t −0.21, n 2352) with the Monday–Tuesday excess return. By weekend-move quintile that excess is +0.40 %, −0.86 % (t −2.8), +0.02 %, +0.27 % and +0.17 %, with no order. Monday–Tuesday moves show no cleaner pattern into Wednesday–Thursday.
- **F5:** The tested idea's grading by the volatility ratio is not there. After weekend falls, the Monday–Tuesday excess return is +0.49 % (t 1.35, n 359) in the lowest weekend/prior-week volatility tercile, −0.85 % (t −2.05, n 349) in the middle and −0.15 % (t −0.40, n 359) in the highest. This matches step 5's failed upper-minus-lower check (−0.11 %) and the book's Sharpe of 0.20, below holding's by 0.35.
- **F6:** Among the 24 hours of the day, the bars starting at 21:00 and 22:00 UTC have the largest excess hourly returns: +4.9 bp (t 6.1) and +3.8 bp (t 5.0), about 17,400 bars each.
- **F7:** The two-hour return from 21:00 to 23:00 UTC is strongest in specific years, coins and weekdays:
- **F8:** That evening rise is largest after a fall over the previous 8 hours. By the prior 8-hour move scaled by volatility, the quintiles earn 8.2 bp (t 3.0), 5.8, 1.9, 3.8 and 2.5 bp. The linear slope, however, has t of only −1.1 (n 16,093).

## Ideas
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.g1_weekly-trend-carries-into-weekend` (from F1, F2, F3, F4): A coin's return over the past 5 days, read at the start of the weekend, continues over the following 2 days in the same direction. The larger the 5-day move relative to the coin's usual 5-day move, the larger the weekend move that follows.
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.g2_late-evening-rebound-after-falls` (from F6, F7, F8): A coin that fell over the previous 8 hours rises over the 2 hours following 21:00 UTC. The larger the fall relative to the coin's usual 8-hour move, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

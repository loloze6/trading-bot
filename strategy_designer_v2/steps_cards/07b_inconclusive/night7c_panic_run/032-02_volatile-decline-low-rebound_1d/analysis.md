---
line: 7.b inconclusive
backtest: 032-02_volatile-decline-low-rebound_1d
idea tested: 032-02_volatile-decline-low-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3948 USD
---
## Findings
- **F1:** The tested effect points the right way but is small against its noise. On folds B and C, the regime's 5-day grid cases number 61. Their mean unusual 5-day move is +0.6 % (t 0.34) and their median is +1.6 %, with 59 % of cases positive. Step 5's own measure over all folds is +2.05 % with t 0.75, on 42 cases across 27 days.
- **F2:** The effect is mixed across periods and coins. Window w17 shows +5.3 % (t 2.04, 11 cases) and window w16 shows −8.2 % (t −1.41, 12 cases). By coin, XMR shows +4.6 % (8 cases) and BTC +2.9 % (9 cases), while LTC shows −1.8 % (12 cases) and ZEC −1.6 % (9 cases).
- **F3:** The rebound appears sooner than the plan's 5 days and fades by day 5. On fresh breaks inside the regime (39 cases, day-clustered), the unusual move is +3.5 % after 1 day (t 1.29), +2.3 % after 2 days (t 1.12), +2.8 % after 3 days (t 1.11) and −1.3 % after 5 days (t −0.26). The regime's grid cases also gain +4.9 % on average over 1 day.
- **F4:** Deeper breaks are followed by larger rises, more clearly over the first day than over five.
- **F5:** Outside the falling, wide-range regime, a monthly low is followed by further falling, so the regime filter carries the effect.
- **F6:** The test is starved of cases, not of size. The book trades only 0.0037 times per coin-day and is in a position on 7 % of coin-days, yet the total move of +2.66 % per case is 13.8 times the 0.19 % cost of a trade. More coins would add cases without making the move smaller than the cost.

## Ideas
- `032-02.b1_volatile-decline-low-rebound-more-coins` (from F1, F2, F6): In a coin that has fallen over the past 30 days and whose daily high-low ranges over that month are wide compared with its own past year, a close below its lowest low of the prior 30 days is followed by a rise over the next 5 days. The further that close sits below the prior 30-day low, the larger the rise.
- `032-02.b2_volatile-low-next-day-rebound` (from F3, F4, F5): In a coin that has fallen over the past 30 days and whose daily high-low ranges over that month are wide compared with its own past year, a close below its lowest low of the prior 30 days is followed by a rise over the next 1 day. The further that close sits below the prior 30-day low, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.e profitable but not proven
backtest: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d
idea tested: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3869 USD
---
## Findings
- **F1:** The book earns almost all of its gain on one bar, the Friday-close bar held into Saturday, and most of that gain is timing rather than the market's rise. The mean per-bar position gain is 0.2671 % on Friday bars, 0.0836 % on Saturday bars and between −0.009 % and +0.006 % on every other weekday. The market's own rise accounts for only 0.0098 % of the 0.0483 % mean gain per bar.
- **F2:** The idea is present in the data, but as a jump at the top rather than a straight line. Fridays sorted into quintiles by the 14-day rise in usual moves give 2-day returns of −0.14 %, −0.26 %, +0.55 %, +0.66 % and +1.81 % (top quintile t 6.2, about 409 cases each). That shape fits the plan's linear slope test on the self-standardised forecast poorly, which gave slope t 1.29. The forecast terciles still rise in order: +0.78 %, +1.12 %, +1.44 %.
- **F3:** The weekend effect sits almost entirely in the Saturday leg. After a 14-day rise, Saturday returns +0.90 % and Sunday +0.27 %; after a 14-day fall, Saturday returns −0.11 % and Sunday +0.04 %. The next-day return after a rise minus after a fall has Welch t 5.85 on Friday closes and at most 1.70 on any other weekday's close.
- **F4:** The same rise measured at Thursday's close also shows up on Saturday. After a rise, the Saturday leg is +0.69 % against +0.13 % after a fall, and the Friday leg is +0.39 % against +0.16 %.
- **F5:** The 14-day lookback is the strongest of those tried for the Friday-to-Sunday move. Top-tercile minus bottom-tercile Welch t is 1.91 for 3 days, 2.02 for 7, 5.34 for 14, 4.15 for 28 and 1.43 for 56 days.
- **F6:** Measured as an excess over each coin's 2-day mean, the effect is sure. Friday cases with a 14-day rise beat that mean by +0.91 % per case, with t 3.35 when the cases of each day are summed (265 days).
- **F7:** The gain is not one coin or a few trades, but it is uneven across years.

## Ideas
- `031-01.g1.g1.g1.d1.e1_two-week-rise-lifts-saturday` (from F1, F2, F3, F6, F7): The larger a coin's 14-day rise, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday, the next 24 hours.
- `031-01.g1.g1.g1.d1.e2_thursday-rise-foreshadows-saturday` (from F3, F4): The larger a coin's 14-day rise, measured in its usual daily moves at Thursday's close (UTC), the more it rises over the following Saturday.
- `031-01.g1.g1.g1.d1.e3_four-week-rise-carries-weekend` (from F5, F1): The larger a coin's 28-day rise, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday and Sunday together.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

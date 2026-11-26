---
line: 7.g patterns
backtest: 031-01_wide-flat-day-ends-uprun_1d
idea tested: 031-01_wide-flat-day-ends-uprun
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4320 USD
---
## Findings
- **F1:** Wide-range days (range at least the 20-day average) that close in the lowest fifth of their own range are followed by a next-day move of +0.752 % above the coin's normal daily drift (t 3.12, 1377 cases on 583 days). On the same wide days, closes in the highest fifth are followed by −0.166 % (t −0.79). On narrow days, closes in the lowest fifth are followed by only +0.075 % (t 0.44).
- **F2:** Over all days, the lowest fifth of close position in the range is followed by +0.343 % the next day (t 2.27, 3479 cases, 1287 days), falling to −0.192 % for the highest fifth (t −1.47). Taking the side opposite to where the close sits in the range earns +0.142 % a day (t 2.33, 17379 cases), positive on all six coins (t from 0.85 for ZEC to 4.01 for XMR).
- **F3:** The move after a low close lasts one day only: at 2 days the lowest fifth is +0.04 % (t 0.14), and at 3 days it is −0.20 % (t −0.47).
- **F4:** The close-position effect weakens over time. Its yearly t is 1.92 in 2019 and 2.62 in 2020, then 0.27 in 2022, −0.20 in 2024 and −1.32 in 2025, although the lowest-fifth next-day move is positive in 6 of 8 years.
- **F5:** The tested situation shows no reversal. Wide days that closed flat after a 5-day rise were followed by a 5-day unusual move of −0.49 % in the coin (t −0.29, 32 cases). Wide days after a rise that closed in the top third were followed by +1.04 % (t 0.73, 127 cases), and the range ratio's rank correlation with the scaled 5-day move is +0.063: wide days lean towards continuation, not reversal.
- **F6:** The book's 627 position bars held a mean allocation of −0.53 while the coin rose +0.084 % on the next bar: the shorts sat against the coins' small next-day rise.
- **F7:** F1's next-day unusual move of +0.75 % is about 4 times the 0.19 % cost of a trade, against the tested idea's −1.24 % per case in the wrong direction. F1 has the largest t among roughly 30 groupings examined, but the decay in F4 makes it less sure than its t alone suggests.

## Ideas
- `031-01.g1_wide-day-low-close-rebounds` (from F1, F2, F3, F4, F7): After a day whose high-low range is wide compared with its average daily range over the past 20 days and whose close lands near the day's low, the coin rises over the next 1 day. The wider that day's range against its 20-day average and the closer its close to the low, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

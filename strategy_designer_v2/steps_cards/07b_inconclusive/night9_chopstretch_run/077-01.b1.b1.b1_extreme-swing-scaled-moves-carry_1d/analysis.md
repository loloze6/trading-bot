---
line: 7.b inconclusive
backtest: 077-01.b1.b1.b1_extreme-swing-scaled-moves-carry_1d
idea tested: 077-01.b1.b1.b1_extreme-swing-scaled-moves-carry
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3937 USD
---
## Findings
- **F1:** The test's own result is on the side the idea predicts but far from the bar, and no more data exists: the |forecast|-weighted signed unusual 7-day move is +0.0083 with a day-clustered t of 0.52 on all four folds and all 19 coins. Its size is +0.20 % per case (t 0.31, 572 days, 908 cases), a strength of 0.013 of a usual move against about 0.05 for real ideas, and 0.9 times the cost of a trade.
- **F2:** In folds B and C the forecast's cases carry more, but not clearly: 168 cases on 75 days, signed unusual 7-day move +1.90 % (t 1.96, cases counted separately) and 14-day move +4.37 % (t 2.46). The full-data mean is 0.20 %, so folds A and D must carry about nothing or reverse.
- **F3:** The plan measured something other than the idea's move against its own swing. The plan first standardised the swing-scaled move over its past 60 values and then cubed it. That forecast disagrees in sign with the raw 14-day return in 30-day-swing units on 15 % of cases (correlation 0.85). On the raw swing-scaled move, weighted by its size, the 7-day carry is +5.88 % with a day-clustered t of 2.24 (143 cases, 61 days).
- **F4:** On the raw swing-scaled move the carry is graded, but it grows roughly in proportion to the move, not faster. At 7 days the terciles of |move| carry +0.60 % (t 0.41), +2.72 % (t 1.69) and +5.29 % (t 1.92). The cubic forecast's quintiles instead jump around: −1.75 %, +1.58 %, +2.83 %, −1.03 %, +7.78 %.
- **F5:** The cubic forecast's strongest cases are almost all on one side. Its top quintile has 32 longs and 2 shorts, and its +7.78 % carry (t 3.18) comes from the longs. On the raw swing-scaled move both sides carry at 7 days: longs +3.11 % (t 1.42, 37 days) and shorts +2.57 % (t 1.58, 37 days), as the brief requires.
- **F6:** The effect is mixed across years, which helps explain the weak full-data t. Weighted 14-day carry on the raw move is −3.9 % in 2018 (t −0.50), −3.9 % in 2019 (t −1.59), +7.0 % in 2020 (t 1.78) and +13.9 % in 2021 (t 2.58).

## Ideas
- `077-01.b1.b1.b1.b1_swing-scaled-move-carries-proportionally` (from F1, F3, F4, F5, F6): In a choppy, calm market, a coin's 14-day return measured in units of its own daily swing over the past 30 days carries on the same way over the next 7 days, up or down, by an amount that grows in proportion to the size of that swing-scaled move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

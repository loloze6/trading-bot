---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean_1d
idea tested: 032-01.b1.b1.e2.d1.d1_chop-continuation-with-monthly-lean
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6032 USD
---
## Findings
- **F1:** Most of the coins' falls are followed by a next-day bounce that grows with the size of the fall, which the tested idea does not use: sorting down days into sextiles by the day's return over its 30-day daily standard deviation, the next day's unusual return falls steadily from the largest falls to the smallest (+0.91 % with t 3.54 over 532 cases, then +0.52 % with t 2.32, +0.13 %, +0.20 %, +0.07 %, +0.09 %), but taking the cases of one day together the largest-fall bounce has a t of only 1.79 over 172 days, so the evidence is weaker than the plain t says.
- **F2:** The bounce after the largest falls grows with how agitated the coin is, measured as its 30-day daily standard deviation over that measure's own 90-day mean: −0.10 % (t −0.23, 124 cases) when calm, +1.15 % (t 2.67, 123) in the middle, +2.26 % (t 3.52, 124) when agitated.
- **F3:** The bounce is one-sided and lasts about two days: the largest up-day quartile shows no next-day reversal (−0.01 %, t −0.03, 603 cases) against +0.99 % (t 3.84, 507) after the largest down-day quartile, and on a non-overlapping 2-day grid the largest down-day quartile is followed by +1.07 % (t 2.92, 388 cases), grading down to −0.39 % for the smallest falls.
- **F4:** The book stands against this bounce: after the largest falls it holds a mean position of −0.075 of the book (t −3.31, 532 bars), and its trades split by side as long +4.86 % mean (1028 trades) against short −1.59 % mean with a −2.42 % median (1143 trades).
- **F5:** The tested continuation (choppy 30 days, 7-day move the same way as the 30-day return) grades with the move's size on the 7-day grid: +1.56 % small (t 1.19), +3.65 % mid (t 2.81), +5.88 % large (t 4.40). In trending 30 days the same aligned moves do not continue (−1.91 %, −2.54 %, −0.38 %), and its strength sits in 2020–2021 (+5.4 % t 3.49 and +6.5 % t 3.97) rather than 2018–2019 (+1.8 % t 1.06, +0.9 % t 0.81).
- **F6:** The book's gain is concentrated in a few days: its best 5 % of days make 342 % of its summed daily gain, and its best 1 % of days average +13.3 % while the coins move +4.1 %. Its worst 1 % average −9.5 % while the coins move −1.6 %. This is consistent with the Calmar failure (0.59).

## Ideas
- `032-01.b1.b1.e2.d1.d1.g1_agitated-large-fall-next-day-bounce` (from F1, F2, F3, F4): When a coin falls on a day by a large amount compared with its 30-day daily swings, it rises over the next 1 to 2 days. The bounce is larger the larger that scaled fall, and larger the more the coin's current 30-day swings exceed their usual level over the past 90 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

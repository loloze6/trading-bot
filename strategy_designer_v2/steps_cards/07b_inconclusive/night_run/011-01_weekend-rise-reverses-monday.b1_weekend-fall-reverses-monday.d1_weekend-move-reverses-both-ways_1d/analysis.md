---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3351 USD
---
## Findings
- **F1:** The reversal belongs to Sunday alone: the signed 2-day move against the day's own move is 0.0082 (t 5.08, n 2051) after Sunday, while every other weekday lies between −0.0036 and +0.0008. Sunday minus the other days is 0.0079, 0.0151 and 0.0084 (Welch t 2.44, 4.78, 2.60) in the three lower |move| quartiles.
- **F2:** The effect is not graded at the top, which is why the supporting check failed. By |forecast| quartile, the signed 2-day reversal is 0.0037, 0.0152, 0.0125 and 0.0016 (616 cases each). In the largest |move| quartile, Sunday minus the other days is only 0.0011 (t 0.26). The median-split difference of −0.00084 is small next to these swings.
- **F3:** In the middle quartiles both sides reverse. After a fall the signed reversal is 0.0109 and 0.0092 (t 2.60, 2.05); after a rise it is 0.0163 and 0.0104 (t 3.94, 2.55). In the largest quartile neither side reverses (fall 0.0032 with t 0.49, rise −0.0012 with t −0.22).
- **F4:** The main measure is positive in every coin, but alone none of them clears the bar except XMR (t 2.61). BTC sits at t 0.19 and the others between 0.50 and 1.34. It is positive in 7 of 8 years, with 2023 at −0.0014, so the pooled t of 2.75 comes from a small effect spread widely, not from one pocket.
- **F5:** Most of the reversal shows on Monday, and it does not decay afterwards. The signed reversal is 0.0056 (t 4.71) over 1 day, 0.0082 (t 5.08) over 2 days, 0.0086 over 3 days and 0.0087 over 5 days. Tuesday alone adds 0.0029 (t 2.79).
- **F6:** Weekend volume does not grade the reversal: the signed 2-day reversal is 0.0112, 0.0041 and 0.0090 across Sunday volume terciles (low to high, relative to the 28-day mean).

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.b1_weekend-reversal-wider-coins` (from F1, F2, F4): A coin's Monday-and-Tuesday return runs against its weekend (Sunday close-to-close) move: after a weekend rise it falls over the next 2 days, and after a weekend fall it rises over the next 2 days. The larger the weekend move relative to the coin's usual daily move, the larger the move back.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.b2_moderate-weekend-moves-reverse` (from F1, F2, F3, F5): A coin's Monday-and-Tuesday return runs against its Sunday close-to-close move when that move is large against the coin's 20-day usual daily move, but not the very largest. Within that range, the larger the Sunday move in usual daily moves, the larger the move back over the next 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

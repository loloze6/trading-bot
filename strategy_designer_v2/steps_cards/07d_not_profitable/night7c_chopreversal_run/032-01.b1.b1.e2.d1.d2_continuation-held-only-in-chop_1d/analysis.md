---
line: 7.d confirmed, not profitable
backtest: 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop_1d
idea tested: 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4021 USD
---
## Findings
- **F1:** The continuation is carried entirely by chop cases where the scaled 7-day move points the same way as the coin's 30-day net move: on the non-overlapping 7-bar grid in chop, those cases give an unusual move of +3.74 % per case (t 4.89, 344 cases), while cases where the 7-day move runs against the 30-day move give +0.18 % (t 0.20, 268 cases); with the forecast's own sign, the aligned cases give +3.77 % (t 4.89) against +0.32 % (t 0.48).
- **F2:** The 30-day direction is not an effect of its own. Trading the 30-day direction in chop gives +2.03 % (t 3.49, 612 cases), but on the cases where it disagrees with the 7-day move it gives about −0.18 %. All of its gain comes from the cases where both agree, which fits the idea's own theory: a 7-day push inside the chop range's net drift is the one that continues.
- **F3:** The book's falls come from the positions taken against the 30-day move. On the chained daily book before costs, positions aligned with the 30-day move earn 0.079 % a day (sd 1.22 %, deepest fall −15.5 %). Positions against it earn 0.0006 % a day (sd 1.12 %, deepest fall −33.5 %). The whole book earns 0.080 % a day with a −27.0 % deepest fall. Leaving out the against side keeps all the gain, roughly halves the fall (the failing Calmar) and cuts the days in a position, which raises the failing mean per day in a position.
- **F4:** Inside the aligned chop cases the effect is graded by the scaled 7-day move: the unusual move is +1.96 % (t 1.58), +3.78 % (t 2.70) and +5.49 % (t 4.14) across |z| terciles (about 115 cases each). The strongest tercile's move is about 29 times the 0.19 % cost of a trade.
- **F5:** The book stays in a position outside chop on 38 % of its position days (grid: 15.5 % of bars non-chop with a position), and those days earn only 0.0085 % a day against 0.071 % for days held in chop. Outside chop the scaled-week continuation reverses: −1.69 % unusual per case (247 cases), and −3.69 % (t −2.36, 55 cases) when the 7-day move is against the 30-day move.
- **F6:** The gain is uneven across windows. The grid unusual move ranges from −2.10 % (w12) to +6.41 % (w16), with 5 of 12 windows at or below 0. Daily, the book's 12 window means range from −0.09 % to +0.24 %.

## Ideas
- `032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift` (from F1, F2, F3, F4, F5): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings tends to be followed by a move the same way over the next 7 days, only while that 7-day move points the same way as the coin's 30-day net move and the past 30 days are still going back and forth at each day's close. The larger that scaled 7-day move, the larger the following move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

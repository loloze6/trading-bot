---
line: 7.d confirmed, not profitable
backtest: 032-01.b1.b1.e2.d2_chop-continuation-with-month_1d
idea tested: 032-01.b1.b1.e2.d2_chop-continuation-with-month
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3999 USD
---
## Findings
- **F1:** The Calmar fails because of costs more than because of the signal. Rebuilt from positions and closes before costs on folds B and C, the book has a Sharpe of 1.25, a yearly return of +41.0 % and a deepest fall of −23.7 %, a Calmar of 1.73. The recorded book after fees has a yearly return of +19.1 % and a Calmar of 0.59. Its 2171 trades, at 0.19 % each, take more than half the yearly return while the falls stay about as deep.
- **F2:** Positions carried after the regime has ended are what lose. Shorts held outside the regime lose on average (−0.071 % a bar, −1.03 summed, 1451 bars), while shorts inside it gain (+0.126 % a bar, +2.31, 1835 bars). Shorts held 1 to 7 bars after the last regime bar lose −0.08 % a bar (904 and 366 bars). Only 55.7 % of the bars in a position are regime bars, because of the 7-bar minimum holding.
- **F3:** Removing the shorts held outside the regime gives the best version tested, before costs. The Calmar rises from 1.73 to 2.38, the deepest fall shrinks from −23.7 % to −20.2 %, the yearly return rises from 41.0 % to 48.1 % and the Sharpe from 1.25 to 1.48. Holding only on regime bars gives a Calmar of 1.91 and a deepest fall of −18.2 %.
- **F4:** The deepest fall (−23.7 %, 333 days, from w11) came while the coins drifted down (−0.09 % a day) in a choppy state (mean 30-day efficiency ratio 0.19). Its losses came from longs inside the regime (−0.85 summed, 389 bars), longs outside it (−0.43) and shorts outside it (−0.31). Shorts inside the regime gained (+0.12).
- **F5:** The condition is not an effect of its own. On non-overlapping 7-day grid cells outside the regime, following the 30-day direction earns between −2.0 % and +2.9 % (t from −1.6 to +1.6; 65 to 107 cases per cell), and it is negative at mid and high volatility. Inside the regime the same direction earns +2.0 % to +7.0 % (t up to 3.5). The follow-through belongs to the choppy state only.
- **F6:** The effect grows with the strength of the case. On regime grid cases, the unusual 7-day move by tercile of the absolute forecast is +0.95 % (t 0.88), +2.10 % (t 1.94) and +4.13 % (t 3.85), with about 182 cases each. Both sides carry it: shorts +2.56 % (t 3.29, 275 cases) and longs +2.24 % (t 2.28, 270 cases).

## Ideas
- `032-01.b1.b1.e2.d2.d1_chop-continuation-while-chop-lasts` (from F2, F3, F4, F5, F6): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings tends to be followed by a move the same way over the next 7 days, only while that 7-day move points the same way as the coin's 30-day net move. The follow-through lasts only as long as the 30 days stay choppy and the week still agrees with the month. The larger the scaled 7-day move, the larger the following move, over the days the chop lasts.
- `032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation` (from F1, F6): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings tends to be followed by a move the same way over the next 7 days, only while that 7-day move points the same way as the coin's 30-day net move. The move that follows is large mainly after the largest scaled 7-day moves, growing faster than in proportion to their size.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

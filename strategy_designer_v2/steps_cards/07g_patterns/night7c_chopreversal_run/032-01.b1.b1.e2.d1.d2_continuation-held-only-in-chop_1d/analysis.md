---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop_1d
idea tested: 032-01.b1.b1.e2.d1.d2_continuation-held-only-in-chop
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4185 USD
---
## Findings
- **F1:** The next day's return grows with the size of today's fall counted in 30-day daily swings. On 3188 down days, the slope of the next-day demeaned return on the scaled fall is 0.00669 per unit (t 4.60). By bucket, a scaled fall between -2 and -3 is followed by +1.44 % (t 3.21, n 125), between -1.5 and -2 by +0.67 % (t 1.90, n 218), and an up day by -0.29 % (t -3.29, n 3335).
- **F2:** After a scaled fall of 1.5 or more, the next-day rebound depends on where the day closed in its range. A close in the bottom fifth of the high-low range is followed by +1.59 % (t 3.96, n 213), a close at 0.2 to 0.5 by +0.70 % (t 1.43, n 144), and a close in the upper half by -0.04 % (n 15).
- **F3:** The next-day rebound after a scaled fall of 1.5 or more does not depend on the regime and holds across the data. It is +0.98 % in chop (efficiency ratio 0.3 or below, t 2.81, n 250) and +1.58 % outside it (t 2.73, n 122). It is positive on all 6 coins (+0.61 % to +1.54 %) and in 11 of 12 windows.
- **F4:** When the 30-day efficiency ratio is between 0.15 and 0.3, the next 7 days follow the sign of the 30-day move by +3.36 % demeaned (t 3.89, n 289 non-overlapping cases). This is larger than at a ratio of 0.15 or below (+0.86 %, t 1.10, n 323) and above 0.3 (+0.41 %, t 0.32, n 179). It is positive on all 6 coins and in 9 of 12 windows.
- **F5:** The tested 7-day continuation reverses outside chop. Signed by the 7-day move, the next 7 days are -1.47 % at an efficiency ratio of 0.3 to 0.45 (t -1.13, n 179) and -3.70 % at |scaled move| ≤ 0.5 with a ratio above 0.3 (t -2.62, n 82). Outside chop, down weeks are followed by +3.12 % (t 2.26, n 115).
- **F6:** Inside chop, the tested continuation is larger after larger scaled 7-day moves. It is +1.67 % for |z| ≤ 0.5 (n 268), +3.38 % for 1 to 1.5 (n 100) and +6.20 % for 1.5 to 2 (t 2.64, n 40). Over all bars, it fades as the coin's 30-day volatility rises: +2.57 % in its calmest quartile (t 2.51) against -0.36 % in its most volatile quartile (t -0.31).
- **F7:** In the book's trades, longs gained and shorts lost in every quartile of the entry forecast. Longs made +1.41 % to +5.16 % and shorts -1.42 % to -3.66 %, net per trade. In the bars, chop weeks continued on both sides (up +2.47 %, t 2.91; down -1.92 %, t -2.43), so the shorts' losses come from the trades, not from a one-sided effect in the bars.

## Ideas
- `032-01.b1.b1.e2.d1.d2.g1_scaled-daily-fall-rebounds` (from F1, F3): The larger a coin's one-day fall counted in its 30-day daily swings, the higher the coin tends to close over the next day, compared with its usual daily move.
- `032-01.b1.b1.e2.d1.d2.g2_close-at-low-next-day-bounce` (from F2, F1): After a coin's one-day fall, the nearer that day's close sits to the day's low, the larger the coin's rise over the next day.
- `032-01.b1.b1.e2.d1.d2.g3_monthly-drift-persists-in-chop` (from F4): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 30-day move counted in 30-day daily swings tends to be followed by a move the same way over the next 7 days. The larger that scaled 30-day move, the larger the following move.
- `032-01.b1.b1.e2.d1.d2.g4_trending-market-weekly-fall-reverses` (from F5): When a coin's past 30 days have moved steadily in one direction compared with the sum of its daily moves, its 7-day fall counted in 30-day daily swings tends to be followed by a rise over the next 7 days. The larger that scaled fall, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

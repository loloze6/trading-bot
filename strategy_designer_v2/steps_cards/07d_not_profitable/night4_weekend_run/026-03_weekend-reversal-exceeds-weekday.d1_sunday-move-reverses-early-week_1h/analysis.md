---
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3729 USD
---
## Findings
- **F1:** All of the book's edge comes from Sundays whose move went against Saturday's. Those 1311 cases gained +1.03 % per case over 48 hours (t 5.30), or +0.36 % per case on the actual positions, summing to +4.70. The 1079 cases where Saturday and Sunday moved the same way gained −0.01 % (t −0.02), or −0.04 % on the positions, summing to −0.38. They pay the 0.19 % trade cost on every bet and add only noise to the falls.
- **F2:** Regressing the next 48 hours on both days shows they pull in opposite directions. Sunday's 24-hour return reverses (slope −0.154, t −4.09), while Saturday's continues (slope +0.104, t 2.79), over 2355 coin-weeks. Sunday minus Saturday gives a slope of −0.129 (t −5.07); the 48-hour weekend sum gives only −0.024 (t −0.87).
- **F3:** The edge is graded on Sunday's move minus Saturday's, read in the bet's direction. The 48-hour gain rises across quintiles from −0.23 % (t −0.68) to +0.13 %, +0.79 %, +0.89 % and +1.34 % (t 2.98), about 471 cases each. A pure Sunday reversal with no counter-Saturday is worth nothing.
- **F4:** The book sizes up exactly where the edge is weakest. The top quintile of |forecast| holds a mean position of 0.98 but gains only +0.13 % per case, below the 0.19 % cost. The middle quintiles hold 0.23–0.64 and gain +0.67 % to +0.87 %. Vol-scaling Sunday's move does not fix this: the volatility-scaled quintiles gain +0.16 % to +0.85 % with no rise at the top.
- **F5:** The effect lives in volatile markets. Ranked by the coin's 30-day hourly volatility, the bottom two quartiles gain +0.05 % (t 0.23) and +0.15 % (t 0.56), under the trade's cost. The top two gain +0.89 % (t 3.05) and +1.17 % (t 2.81), about 597 cases each.
- **F6:** The failures show up in the falls and the daily gain. The book's daily chain falls by up to 31.0 % (worst in w13, w12, w9), giving a Calmar of 0.12, and its mean daily return is 0.014 %. Mondays (mean +0.108 %, standard deviation 1.78 %) and Tuesdays (+0.036 %, standard deviation 1.53 %) carry all of the risk. All 40 of the book's worst days fall on Monday (23) or Tuesday (17), so the falls come from the bets themselves, half of them the dead same-direction weekends.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week.d1_sunday-against-saturday-reverses` (from F1, F2, F3, F6): A coin's 24-hour return over Sunday is followed by a larger opposite move over Monday and Tuesday than a 48-hour return of the same size ending on any other weekday, only for the part of Sunday's move that undoes Saturday's: the larger Sunday's 24-hour return minus Saturday's 24-hour return, the larger the opposite move over the next two days.
- `026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week.d2_sunday-reversal-in-turbulence` (from F5, F6): A coin's 24-hour return over Sunday is followed by a larger opposite move over Monday and Tuesday than a 48-hour return of the same size ending on any other weekday, only while the coin's 30-day volatility of hourly returns is high: the higher that volatility and the larger Sunday's 24-hour return, the larger the opposite move over the next two days.
- `026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week.d3_saturday-s-move-continues` (from F2, F3): A coin's 24-hour return over Saturday is followed by a move in the same direction over Monday and Tuesday: the larger Saturday's 24-hour return, the larger the move its way over the next two days.
- `026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week.d4_extreme-sundays-reverse-less` (from F4, F6): A coin's 24-hour return over Sunday is followed by a larger opposite move over Monday and Tuesday than a 48-hour return of the same size ending on any other weekday, only for moderate Sunday moves: the opposite move grows with Sunday's 24-hour return up to about the coin's typical daily move and is smaller after Sunday moves much larger than that.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

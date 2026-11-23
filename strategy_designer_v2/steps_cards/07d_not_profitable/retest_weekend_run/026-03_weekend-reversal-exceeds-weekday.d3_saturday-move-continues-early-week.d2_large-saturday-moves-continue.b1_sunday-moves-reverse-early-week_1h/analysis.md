---
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4575 USD
---
## Findings
- **F1:** The reversal belongs to Monday alone. Over 48 hours from the 00:00 UTC bar, the drift-adjusted move against the past 24 hours is +0.62 % on Monday (t 3.98, 2244 cases). On every other weekday it lies between −0.36 % and +0.21 %, for example Tuesday −0.04 % (t −0.30) and Saturday +0.21 % (t 1.78). This is the weekend effect the theory names.
- **F2:** The vol-target sizing puts the book's size where the effect is absent, and that is why its gain is too small. In the lowest third of each coin's 30-day hourly volatility, Monday cases move +0.00 % (t 0.01, 765 cases) while the book holds |allocation| 0.54. In the middle third they move +0.69 % (t 2.92) at 0.38. In the highest third they move +1.21 % (t 3.40, 719 cases) at only 0.23. So the book earns −0.08 % per case in the lowest third, +0.33 % in the middle and +0.24 % in the highest, only +0.16 % per case overall.
- **F3:** High volatility is not an effect of its own. On Tuesday to Saturday, the same 48-hour move against the past 24 hours in the highest volatility third is −0.00 % (t −0.01, 3784 cases), against +1.21 % on Mondays in that third. The condition therefore only grades the weekend reversal, as the theory's thin-liquidity mechanism says: weekend prices are pushed furthest when the coin is turbulent.
- **F4:** Sizing by the size of Sunday's move does not grade the effect and loses money at the top. By quintile of |Sunday z|, the 48-hour reversal is +0.42 %, +0.79 %, +0.50 %, +0.79 % and +0.62 %, with no rise. The trades with the largest entry forecast (mean |forecast| 17.8, 956 trades) lose −0.60 % net. Trades with mean |forecast| 3.2 to 6.4 gain +0.27 % to +0.36 % net.
- **F5:** The book carries positions far past the two days, which dilutes its mean daily return on days in a position (0.021 % against the required 0.05 %).
- **F6:** Most of the reversal comes within Monday itself. It is +0.46 % over 24 hours (t 4.08, 2265 cases), +0.62 % over 48 hours (t 3.98) and +0.78 % over 120 hours (t 3.19). One day's holding gives the larger move per day in a position (0.46 % against 0.31 % a day over two days).
- **F7:** The short side, after a Sunday rise, carries more of the effect than the long side: +0.86 % (t 3.85, 1142 cases) against +0.38 % (t 1.73, 1102 cases). It is strongest in the highest volatility third, at +1.85 % (t 3.83, 368 cases). That is 9.7 times the 0.19 % cost of a trade, while the lowest third's +0.00 % cannot pay any cost.
- **F8:** The effect is spread across years and coins, not tied to one period. It is positive in 7 of 8 years, all but 2023 (−0.03 %), and positive on all six coins, from +0.18 % (ZEC) to +0.91 % (ETH).

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d1_sunday-reversal-grows-with-volatility` (from F2, F3, F4, F8): A coin's 24-hour return over Sunday, measured against the coin's usual 30-day move, is followed over the next two days (Monday and Tuesday) by a move in the opposite direction, and the higher the coin's hourly volatility over the last 30 days, the larger that reversal.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday` (from F1, F5, F6, F2): A coin's 24-hour return over Sunday, measured against the coin's usual 30-day move, is followed over the next 24 hours (Monday) by a move in the opposite direction, the larger the higher the coin's hourly volatility over the last 30 days.
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d3_sunday-rises-fade-in-turbulence` (from F7, F2, F3): A coin's rise over Sunday, measured against the coin's usual 30-day move, is followed over the next two days (Monday and Tuesday) by a fall, and the higher the coin's hourly volatility over the last 30 days, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

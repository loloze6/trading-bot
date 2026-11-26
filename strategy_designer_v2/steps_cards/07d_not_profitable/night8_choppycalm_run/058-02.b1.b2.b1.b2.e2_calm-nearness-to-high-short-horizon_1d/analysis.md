---
line: 7.d confirmed, not profitable
backtest: 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon_1d
idea tested: 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6148 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.67 against 0.75, Sharpe 0.83, yearly +20.3 %), and the deepest falls are long: -28.6 % over 340 days to the trough (w12 to w14), -26.5 % over 90 days (w9) and -18.3 % over 101 days (w7). On the in-position coin-days inside the four deepest falls, the book averaged -0.24 % a day against +0.49 % elsewhere (2453 against 3075 coin-days). On those days the coin's own 20-day return was -5.2 % against +10.2 %, and its 5-day return -1.8 % against +3.6 %: the book was long calm coins that were sliding.
- **F2:** On the non-overlapping 3-day grid in profile, the excess 3-day return depends on the coin's 20-day return. Where it was below -10 % the excess was -1.43 % (t -2.69, n 423); where it was between -10 % and +10 % it was +0.10 % (t 2.17, n 639); above +10 % it was +1.18 % (t 4.01, n 457). The lowest third of the forecast with a falling 20-day return lost -1.53 % (t -2.46, n 303).
- **F3:** By the 60-day trend in profile (the market profile's trend), the excess 3-day return was +1.45 % in a rising calm market (n 338, 107 days, t_day 1.55), -0.20 % in choppy calm (n 214) and -0.63 % in falling calm (n 458, 141 days). The same rising trend outside the calm profile, without the idea's signal, earned only +0.05 % (n 297, t_day 0.05). The rise therefore comes with calm, not with the trend alone.
- **F4:** Kept only in a rising calm market, the same positions (a gross-minus-0.11 %-per-side rebuild of the book) cut the deepest fall from -30.4 % to -8.1 %. In that rebuild Calmar rose from 0.98 to 2.18, Sharpe from 1.03 to 1.15 and the lowest one-window-left-out Sharpe from 0.80 to 0.91, with 11 % of coin-days in a position. Inside rising calm, though, the forecast's slope was flat (t 0.05; thirds +1.50 %, +1.23 %, +1.61 %).
- **F5:** The idea's gradient lives in falling calm markets: the slope of the excess 3-day return on the forecast there had t 4.76 (n 458), against 0.22 in choppy and 0.05 in rising. Across the whole profile, the quarter of closes farthest below the 20-day high lost -1.28 % over 3 days (t -3.14, n 380), and the nearest quarter gained +1.29 % (t 3.16, n 380). A long-only book holds the far, losing side of this gradient through the falls.
- **F6:** Staying out while the 20-day return is negative raised the rebuilt Calmar from 0.98 to 1.59, cut the deepest fall from -30.4 % to -22.2 % and raised the lowest one-window-left-out Sharpe to 1.04. The condition alone earns part of this, though: outside the profile a positive 20-day return earned +0.45 % (t 1.14, n 583), against about +1.0 % inside it. Inside the condition the forecast's slope was flat (t -0.05). This is partly momentum of its own, so it is not proposed as a repair.

## Ideas
- `058-02.b1.b2.b1.b2.e2.d1_rising-calm-near-high-continuation` (from F1, F3, F4): In a rising, calm market, the nearer a coin's close is to its 20-day high, the larger its rise over the next 3 days.
- `058-02.b1.b2.b1.b2.e2.d2_falling-calm-far-from-high-decline` (from F2, F5, F1): In a falling, calm market, the farther a coin's close is below its 20-day high, the larger its fall over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

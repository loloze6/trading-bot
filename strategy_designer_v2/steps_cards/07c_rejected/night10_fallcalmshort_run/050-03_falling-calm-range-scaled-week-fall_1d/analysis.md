---
line: 7.c no effect
backtest: 050-03_falling-calm-range-scaled-week-fall_1d
idea tested: 050-03_falling-calm-range-scaled-week-fall
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3760 USD
---
## Findings
- **F1:** The tested idea shows no effect: on its forecast<0 grid cases the short-direction 3-day unusual move is −0.42 % (t −0.98, 585 cases, 291 days), and its size is +0.07 % per case (t 0.18, 410 days), 0.004 of a usual 7.84 % move. The total move is −0.22 %, below the 0.29 % cost of a trade. My recount on the explore windows gives +0.53 % (t 0.67, 86 cases, 65 days) at 3 days and +1.37 % (t 1.17, 52 cases) at 5 days, with no horizon reaching t 2.
- **F2:** The carry does not grow with the size of the 7-day fall: among profile falls the Spearman correlation of the scaled 7-day return with the unusual forward move is −0.046 at 3 days (86 cases, p 0.68), −0.002 at 5 days (52) and −0.23 at 10 days (23, p 0.28). The most-fallen quintile gives +1.37 % short (t 0.85) and the next −0.28 % (t −0.26), so the grading is not monotone.
- **F3:** In falling calm markets the coin's 3-day move carries on in its own direction over the next 3 to 5 days: the 3-day return in units of the 30-day daily swing correlates with the unusual forward move at rho +0.19 at 3 days (149 cases, p 0.019) and +0.23 at 5 days (86, p 0.037), while the 1-day and 7-day versions do not (rho 0.00 and +0.06 at 1 and 3 days).
- **F4:** On the short side the 3-day fall carries, but not yet surely: the lowest tercile of the scaled 3-day return (mean −1.04 swings) gives a short-direction unusual move of +1.29 % over 3 days (t 1.26, 50 cases, 38 days) and a total of +0.48 %. The middle tercile gives +0.73 % (t 0.81), and the highest tercile (3-day rises) gives −1.70 % (t −1.75), as the coin keeps rising.
- **F5:** A low close in the 20-day high-low range points the same way: the lowest tercile (mean position 0.14) gives a short unusual move of +1.54 % over 3 days (t 1.40, 54 cases), the middle +0.79 % (t 1.21) and the highest −1.42 % (t −1.53); rho +0.13 (162 cases, p 0.09).
- **F6:** The falling calm profile itself does not keep falling: over all its grid cases the coin rose by a total of 1.00 % over 3 days and 2.19 % over 10 days, with a short unusual move of −0.19 % (t −0.36, 189 cases). Coin by coin at 3 days the short unusual move is BTC +0.30 % (t 0.47), XMR −0.61 % (t −0.68) and XRP −0.39 % (t −0.44). The trend's depth adds nothing (60-day return terciles +0.28 %, −0.18 %, +0.14 %).

## Ideas
- `050-03.c1_calm-downtrend-3-day-fall-continues` (from F3, F4, F2): In a falling, calm market, a coin that has fallen over the last 3 days keeps falling over the next 3 days, and falls further the larger its 3-day fall is in units of its 30-day daily swing.
- `050-03.c2_calm-downtrend-near-low-continuation` (from F5, F3): In a falling, calm market, a coin whose close sits near the low of its 20-day high-low range keeps falling over the next 3 days, and falls further the closer its close is to that low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

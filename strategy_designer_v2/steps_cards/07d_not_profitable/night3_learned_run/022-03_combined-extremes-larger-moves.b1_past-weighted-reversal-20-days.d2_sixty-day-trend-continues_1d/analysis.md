---
line: 7.d not profitable
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
idea tested: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4393 USD
---
## Findings
- **F1:** The book's shorts cost it most of holding's gain. Over 17,432 coin-days short, the shorts earned −0.069 % a day before fees. Of that, −0.078 % came from being short coins that drift up, and only +0.009 % from timing. Over 16,188 days long, the longs earned +0.122 % a day, with +0.032 % from timing. As a result the book makes 0.029 % a day against holding's 0.139 %, and fails the mean-return and Sharpe-against-holding measures.
- **F2:** The deepest fall is −78 %, lasting 735 days from w15 to w21. Across those windows the summed daily returns were −1.32 for the book and +0.85 for holding. The book sat about half long and half short (long share 0.49, net position +0.04). On the 20-day grid in w15–21, shorts lost 5.6 % per case against the coin's drift (t −3.06, 202 cases) and longs lost 1.0 % (289 cases). In the other windows, shorts gained 3.5 % (t 3.94, 601 cases) and longs 2.5 % (514 cases).
- **F3:** The forecast is not graded. By forecast sextile, the unusual move in the forecast's direction is −0.45 % for the most negative sixth (mean forecast −16.5) and +1.4 % for the most positive (+18.6). Both are weaker than the moderate sixths (+2.5 % at −8.7, +3.2 % at +10.1). Within each side, the Spearman correlation of |forecast| with that move is −0.03 for longs (803 cases, p 0.42) and −0.06 for shorts (803 cases, p 0.10).
- **F4:** The 60-day trend continues when the coin's 20-day return agrees with it. Longs whose 20-day return is also positive gained 4.9 % per case against drift (8.1 % total, t 2.08, 453 cases). Longs whose 20-day return is negative lost 2.1 % (216 cases). Among longs the move grows with the 20-day return, by quartile: −3.1 %, +0.8 %, +1.9 %, +11.0 % (mean 20-day return −14 %, +2 %, +15 %, +55 %; about 167 cases each).
- **F5:** After a 60-day fall whose last 20 days fell steeply, the coin rebounds. Shorts in the deepest 20-day-return quartile (mean −29 %) saw the coin rise 4.9 % above drift over the next 20 days (8.1 % total, t −2.74, 165 cases). Shorts after milder 20-day falls gained 4.7 % and 5.5 % (t 3.13 and 3.33). On days, coins in their lowest 60-day-return quintile rose 0.25 % a day afterwards, the second highest of the five quintiles.
- **F6:** Longs pay mainly when the coin is volatile. By 20-day-volatility tercile, the unusual move for longs is −0.4 %, +1.9 % and +6.6 % per case (total 2.6 %, 5.0 %, 10.1 %; about 220 cases each). Daily long gains before fees rise from 0.072 % to 0.268 % from the lowest to the highest tercile.
- **F7:** Cost is not the cause. The idea's total move per case is 0.93 % against a round trip of 0.22 %, or 4.2 times the cost. Fees take only about 0.004 % a day, while the shorts lose 0.069 % a day before fees.

## Ideas
- `022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues.d1_confirmed-sixty-day-trend-continues` (from F3, F4, F2): The larger a coin's 60-day return, the more the coin moves in that same direction over the next 20 days, only while its 20-day return has the same sign as its 60-day return, the more so the larger that 20-day return.
- `022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues.d2_trend-except-after-capitulation` (from F5, F3, F1): The larger a coin's 60-day return, the more the coin moves in that same direction over the next 20 days, except after a 60-day fall whose last 20 days fell steeply, where the deeper the 20-day fall, the more the coin rises over the next 20 days.
- `022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues.d3_volatile-sixty-day-rises-continue` (from F1, F6, F2): The larger a coin's 60-day rise, the more the coin rises over the next 20 days, the more so the higher its 20-day volatility.
- `022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues.d4_deep-twenty-day-falls-rebound` (from F5): The deeper a coin's 20-day fall, the more the coin rises over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

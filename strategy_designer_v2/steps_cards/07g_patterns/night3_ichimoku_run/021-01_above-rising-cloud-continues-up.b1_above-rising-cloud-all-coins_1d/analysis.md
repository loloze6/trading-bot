---
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d
idea tested: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4824 USD
---
## Findings
- **F1:** A coin's own 26-day return ranks its next 26 days: on the non-overlapping 26-day grid, the top fifth by 26-day return (ranked within each coin) ends +10.0 % above the coin's normal 26-day drift (strength +0.23), against −5.9 % (strength −0.18) for the bottom fifth, with the middle fifths in between in order (t top minus bottom 3.80, Spearman 0.097, p 0.004, 897 independent cases); 15 of 18 coins have a positive correlation (median 0.077), though not every year does (2018 −0.29, 2024 −0.14).
- **F2:** The same 26-day return ranks the next 10 days even more clearly: Spearman 0.084 (p < 0.0001, 2619 cases), with the top fifth +3.4 % and the bottom fifth −1.9 % against drift (t 4.02); taking the 26-day return over its own volatility gives about the same (Spearman 0.080); and it survives a control for the cloud regime (regression t 3.82, regime t 2.71).
- **F3:** Being above a rising cloud marks better 26-day returns, but how fast the cloud rose does not grade them: trending-regime grid bars earn +7.8 % against the coin's drift, versus −2.3 % elsewhere (t 2.69, 277 against 919 cases), yet inside the trending regime neither the 26-day return (Spearman 0.014, p 0.84) nor the cloud slope (verdict's −0.027) orders the outcome, and at 26 days the regime takes most of the 26-day return's grading (regression t 1.60 for the return, 4.03 for the regime).
- **F4:** Momentum's signal is far larger than a trade's cost: taken in the direction of the 26-day return, the unusual move is +5.6 % per case after rises (strength 0.14, t 2.61, 439 cases) and +3.4 % after falls (strength 0.08, t 1.95, 449 cases), 15 to 25 times the 0.22 % round trip and above the 0.05 strength of F10, while the tested cloud-slope idea's was +1.00 % (strength 0.018) and its book trailed holding (Sharpe 0.56, 0.03 below holding; 3.7 bps a day against the coins' 14).
- **F5:** Contrary to the brief, crossings of thick clouds, not thin ones, are followed by the larger 10-day moves (Spearman of thickness with the absolute 10-day move 0.139, p 0.004, 420 crossings; up-crossings 14.3 % thick against 9.8 % thin), but thickness says nothing about direction (Spearman −0.047, p 0.33), so it is a volatility marker and not a trade.
- **F6:** After an ordinary up day (0 to 1 of its 20-day standard deviation), the next day's return falls 19.6 bps below the coin's mean (t −4.2, 10565 days), but the pattern does not grade across the move sizes and stays under the 22 bps round trip, so it does not count as an idea.

## Ideas
- `021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.g1_26-day-momentum-continues-26-days` (from F1, F3, F4): The larger a coin's return over the past 26 days, the larger its return over the next 26 days, and the lower it lies after its weakest 26-day returns.
- `021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.g2_scaled-momentum-over-ten-days` (from F2, F4): The larger a coin's return over the past 26 days, scaled by its daily volatility over the same 26 days, the larger its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

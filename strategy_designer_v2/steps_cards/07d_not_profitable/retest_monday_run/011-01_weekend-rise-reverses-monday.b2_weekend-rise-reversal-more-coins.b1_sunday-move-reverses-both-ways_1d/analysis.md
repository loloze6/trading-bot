---
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4678 USD
---
## Findings
- **F1:** The check failed on Calmar alone: 0.33 against the 0.75 rule, a yearly return of +9.4 % against a deepest fall of −28.7 %. That fall lasted 907 chained days, from w1 to w9, through losing windows w2 (−7.8 %), w3 (−5.7 %), w4 (−3.4 %) and w7 (−4.9 %). Every other measure passed, including a Sharpe of 0.61.
- **F2:** The effect lives almost entirely in Sundays where the coin's 20-day volatility is high against its 60-day volatility. In the top tercile of that ratio the reversal in the forecast's direction is +1.51 % over 2 days (t 5.07, 879 cases). In the middle and low terciles it is only +0.27 % (t 1.00) and +0.35 % (t 1.53). The book's summed position gain is +6.92 in the top tercile against −0.22 and −0.24 in the other two.
- **F3:** The high-volatility condition is not an effect of its own. On non-Sunday bars in the same top tercile, a 1-day move reverses by only +0.04 % over 2 days (t 0.25, 2750 cases). The Sunday reversal exceeds it by 1.47 % (Welch t 4.42). This fits the brief's theory: a weekend imbalance in an already stressed, thin book is paid more for liquidity.
- **F4:** Trading only the top-volatility-ratio Sundays roughly halves the falls in a weekly chained proxy of the book. The deepest fall goes from −15.4 % to −8.2 % with an almost unchanged yearly return (+15.6 % against +15.1 %), lifting the proxy Calmar from 0.98 to 1.90. This proxy is pooled case gains, not the daily book.
- **F5:** Sizing linearly by the weekend move concentrates the falls without buying more reversal. The top |move| quintile holds a mean |allocation| of 0.88 against 0.49 for the fourth quintile, yet reverses less: +0.90 % (t 3.09) against +1.12 % (t 4.41). The worst 2 % of cases carry a mean |allocation| of 0.91. The worst 5 % of cases make up 53 % of all losses.
- **F6:** Capping the position also improves the falls in the proxy. With the position capped at 0.3 the proxy Calmar is 1.36 (deepest fall −7.9 %); with equal sizing it is 1.28 (−11.2 %); with the tested sizing it is 0.98.
- **F7:** Both sides of the bet reverse, so neither side should be left out. Betting against weekend rises gives +0.77 % (t 4.99, 2574 cases) and betting against weekend falls gives +0.55 % (t 3.75, 2664 cases).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility` (from F1, F2, F3, F4, F7): A coin that moved over the weekend (its Saturday-to-Sunday close-to-close return) moves the other way over the next 2 days (Monday and Tuesday), the larger the weekend move the larger the move back, only while the coin's daily volatility over the last 20 days is high against its last 60 days.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal` (from F2, F3, F5, F6): A coin that moved over the weekend (its Saturday-to-Sunday close-to-close return) moves the other way over the next 2 days (Monday and Tuesday), and the move back is larger the more the coin's 20-day daily volatility exceeds its 60-day daily volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

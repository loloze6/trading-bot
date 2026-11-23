---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4656 USD
---
## Findings
- **F1:** Across all coins, the next day's excess return falls as the day's return grows, in units of the coin's 20-day volatility (Spearman rho −0.046 over 21,371 daily cases, t −6.7); after the 10 % weakest days the next day is +0.30 % (t 2.5) and after the 7th–9th deciles it is −0.24 % to −0.17 % (t −2.6 to −1.7), though the strongest-day decile breaks the slope at +0.16 % (t 1.2).
- **F2:** A coin's 5-day excess return rises with its rising volatility, the ratio of its 20-day to its 60-day daily volatility (rho +0.049, t 2.8, 3,188 non-overlapping cases); the top quintile of the ratio is followed by +1.11 % (t 2.5) and the bottom quintile by −0.76 % (t −1.8).
- **F3:** The same holds for the width of the day's bar, (high − low) / close: rho +0.046 (t 3.2, 4,804 cases), with +1.22 % over the next 5 days in the widest quintile (t 2.7) against −0.40 % in the narrowest. That move is about 5 times the 0.22 % cost of a trade.
- **F4:** The 5-day reversal shows only when volatility is high: among cases above the coin's median 20-day volatility, the prior 5-day return in volatility units predicts the next 5 days with rho −0.061 (t −2.8, 2,104 cases), against rho +0.014 (t 0.6) in low volatility; by year the rho is negative in every year from 2022 to 2025, down to −0.128 in 2025.
- **F5:** The tested forecast does not grade its outcome: among positive-forecast cases the quintiles run −0.11 %, +0.52 %, +0.01 %, +0.63 %, +0.72 % (rho +0.012, t 0.6, 2,489 cases); trades in the lowest entry-forecast quartile net +6.46 % against +3.40 % in the second.
- **F6:** Most of the book's gain is market exposure, not timing: positive-forecast cases beat zero-forecast cases by 0.73 % over 5 days (+0.35 % vs −0.38 %), and on the book's worst and best 2 % days the coins move −9.97 % and +8.65 % against the book's −4.11 % and +4.62 %. The Calmar shortfall comes from 2022 (book −35 % annualised mean) and 2018 (−8 %).
- **F7:** Next-day excess returns differ by weekday: Monday −0.28 % (t −3.5), Tuesday +0.29 % (t 3.2), Wednesday −0.27 % (t −3.1), Friday +0.29 % (t 4.3). These pool 15 coins that trade on the same days, so the t is overstated, and the pattern is not graded.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week.g1_volatility-expansion-precedes-rise` (from F2, F3): The more a coin's 20-day volatility has risen above its 60-day volatility, and the wider its latest daily range relative to its close, the larger its rise over the next 5 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week.g2_high-volatility-weekly-reversal` (from F4): When a coin's 20-day volatility is high for that coin, the lower its 5-day return measured in its own volatility, the larger its rise over the next 5 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week.g3_one-day-reversal-after-drops` (from F1): The more a coin's daily return falls below zero, measured in its 20-day volatility, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3305 USD
---
## Findings
- **F1:** The book earned a mean of 0.000231 a day against 0.001275 for holding the coins, because it was in the market only 31.7 % of bars with a mean position of 0.164; its 0.000428 mean gain per bar splits about evenly into 0.000207 from the coins' own rise and 0.000222 from timing.
- **F2:** In round 1, with the day's move scaled by its 20-day mean absolute move, both tails were followed by higher 5-day returns: +0.0144 (t 2.46, n 199) after the largest down days and +0.0193 (t 3.19, n 199) after the largest up days, against −0.002 to −0.006 in the middle three quintiles.
- **F3:** That U-shape did not survive the idea's own 60-day scaling: the top quintile of absolute scaled move minus the rest was +0.0048 (Welch t 0.64, 161 cases), the slope of the 5-day return on absolute scaled move had t 0.84 (n 803), and the yearly sign flipped (negative in 2020, 2022 and 2024).
- **F4:** The calm-regime part of the tested idea is weak on the grid: after up days, calm bars gave +0.0099 and volatile bars +0.0008 over 5 days (209 and 208 cases), but the slope of the 5-day return on the scaled move within calm bars had t only 0.53 (n 445).
- **F5:** Next-day returns by weekday were highest on Friday (+0.0026, t 2.62) and Tuesday (+0.0037, t 2.46) and lowest on Wednesday (−0.0026, t −1.60), but seven weekdays tested among many angles makes a t of about 2.5 indistinguishable from chance.
- **F6:** Neither the prior 20-day return (slope t 0.74 on 5-day returns) nor the 20-day volatility rank (quintile means 0.002 to 0.008, all |t| below 1.3) graded the next 5 days.

## Ideas
- No ideas: Across the scaled-move tails, absolute move size, volatility rank, prior 5- and 20-day returns, weekday, coin and year, no pattern held under a second definition or stood out enough from the many angles tested to count as more than chance.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

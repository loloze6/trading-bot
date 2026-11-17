---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
idea tested: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5222 USD
---
## Findings
- **F1:** The bounce exists only while the coin's 10-day volatility is above its 60-day volatility. After falls beyond 1.3 usual moves with 10-day over 60-day std above 1, the next-day excess was +0.0141 (t 5.03, n 440) and the summed gain +4.82. After the same falls with the ratio at or below 1, the excess was -0.0050 (t -1.54, n 241) and the summed gain -0.52, even though the position held there was as large (0.94 against 1.04).
- **F2:** The effect grows with that volatility ratio across all active bars. By ratio quartile, from lowest to highest, the excess was -0.0020, +0.0007, +0.0057 and +0.0099 (t -1.15, 0.40, 2.89, 4.17). The summed gain was -1.14, +0.39, +2.25 and +4.02, while summed fees rose from 0.18 to 0.37. The lowest quartile loses the book money outright.
- **F3:** The ratio separates the bounce at every level of 60-day volatility. In each 60-day-std tercile the excess was negative with the ratio at or below 1 (-0.0028, -0.0016, +0.0011) and positive above 1 (+0.0046, +0.0069, +0.0161, with t 2.1, 2.6, 4.7).
- **F4:** The book runs its smallest positions where the effect is largest. By 60-day-std quartile the mean position fell from 0.65 to 0.26, while the excess rose from +0.0014 (t 0.84) to +0.0096 (t 3.88). The result is a mean daily return of 0.00045, against 0.0005 required and 0.00118 from holding, with active bars only 28% of the total.
- **F5:** The book's falls come from large longs after large falls that kept falling. The active bars before the worst 5% of book days had a mean z of -1.47 and a mean position of 0.77, against -0.73 and 0.37 on other bars. They lost 11.9 in summed gain against +17.4 elsewhere. The deepest fall was -0.249 and the Calmar 0.60.
- **F6:** The bounce also shows when the coin's 20-day move is large in units of its usual move. By quintile of the absolute 20-day vol-scaled move, the top quintile (mean 2.03) gave an excess of +0.0098 (t 3.99), and the lowest gave -0.0007 (t -0.35).

## Ideas
- `011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.d1_selloff-bounce-in-rising-volatility` (from F1, F2, F3, F5): When a coin's day-long fall is large compared with its usual daily move over the past 60 days, it rises over the next 1 day, and the larger the fall in units of its usual move, the larger the rise. This holds only while the coin's 10-day volatility is above its 60-day volatility, and the rise is larger the higher that ratio.
- `011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.d2_selloff-bounce-after-large-swings` (from F6, F4): When a coin's day-long fall is large compared with its usual daily move over the past 60 days, it rises over the next 1 day, and the larger the fall in units of its usual move, the larger the rise. This holds only while the coin's 20-day return is large in units of its usual daily move, and the rise is larger the larger that 20-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3442 USD
---
## Findings
- **F1:** The book holds a position only from the Sunday close to the Monday close, so it is flat six days in seven. Mean absolute position is 0.406 on Sundays against 0.000–0.0008 on every other weekday, and the mean gain is 0.001245 on Sunday bars and about 0 on all others. The book's mean daily return is therefore 5.6e-05, against 0.00119 for holding the coins and against the required 0.0005.
- **F2:** The move back does not end after one day; it keeps building through day 3. On the 1,817 Sunday cases, the reversal net of each coin's mean is 0.0059 (1 day) vs 0.0123 (3 days) in the largest-fall quintile, 0.0093 vs 0.0123 in the fourth quintile, and 0.0017 vs 0.0094 in the largest-rise quintile. The one-bar hold keeps less than half of it.
- **F3:** Sizing is inverted at the extremes. The largest-rise quintile carries the biggest positions (mean |position| 0.81, mean |forecast| 14.9) but reverses least over 1 day (0.0017) and loses money (mean gain −0.0021). In the top quartile of |z| the 1-day reversal is about 0 in both trend states (−0.0009 and −0.0008), while the middle quartiles reverse most (0.015–0.018 in down-trends).
- **F4:** The losing side is a weekend rise while the coin's 30-day return is up. Those 526 cases show a 1-day reversal of 0.00098 (t 0.42) and a mean book gain of −0.0019. Weekend rises in 30-day down-trends reverse by 0.0101 (t 3.86, n 439) and falls in down-trends by 0.0085 (t 3.41, n 435).
- **F5:** The reversal rises with the coin's 20-day volatility, measured as the 1-day reversal net of each coin's mean. It is 0.0007, 0.0057 and 0.0114 from the lowest to the highest volatility tercile (3-day: 0.0033, 0.0086, 0.0151). The low-volatility tercile has a negative book gain (−0.0007).
- **F6:** The 60 worst book days average −9.2% for the book while the coin's own day averages +1.6%, and the coin rose on 58% of them. The deepest falls are shorts held into a continuing rise, which is what drags Calmar to 0.061.
- **F7:** The effect has faded over time. The raw 1-day reversal by year runs 0.0086 / 0.0052 / 0.0158 / 0.0116 in 2018–2021 and −0.0001 / 0.0021 / 0.0022 / −0.0005 in 2022–2025. The book's mean daily return is negative in every year from 2021 to 2025.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.d1_weekend-reversal-in-downtrends` (from F2, F4, F6, F1): A coin's return over the next 3 days (Monday to Wednesday) runs against its Sunday close-to-close move: after a weekend rise it falls and after a weekend fall it rises. The larger the weekend move relative to the coin's usual daily move, the larger the move back, only while the coin's 30-day return is negative.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.d2_volatile-weekends-reverse-more` (from F5, F3, F2): A coin's return over the next 3 days runs against its Sunday close-to-close move. The size of that move back, in price terms, grows with the coin's 20-day volatility of daily returns, so the same weekend move scaled to usual size is undone more when the coin has been volatile.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.d3_extreme-weekend-moves-continue` (from F3, F6): A coin's moderate weekend move (Sunday close-to-close, up to roughly one to two usual daily moves) is undone over the next 3 days. The larger such a moderate move relative to the coin's usual daily move, the larger the move back, while its most extreme weekend moves continue in their own direction over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

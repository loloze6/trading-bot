---
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
idea tested: N2-04_slow-and-fast-momentum
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3516 USD
---
## Findings
- **F1:** Almost all of the book's gain came from days when both the 60-day and the 20-day return were up. Those 3,047 coin-days carried 9.23 of the 13.11 summed daily book return, with a book mean of 0.003028 and a coin mean of 0.003821. Every other state had a book mean near 0 (between −0.000036 and −0.000012), and the 60-up/20-down state had a negative coin mean of −0.001731.
- **F2:** The book earns from timing more than from the market's own rise. Of its mean daily return of 0.000754, only 0.000252 is exposure times the coin's drift and 0.000553 is timing (t 3.64), at a mean allocation of 0.21. The coin rose 0.002937 a day while held against 0.000311 while flat (n 5,816 vs 11,564; Welch t 3.21), even though the plan's 20-bar excess return was not significant (mean 0.019, t 0.85, 269 blocks).
- **F3:** The effect is graded. On held days, the next day's coin return rose with the forecast quartile: 0.0019, 0.0019, 0.0033 and 0.0047 at mean forecasts of 4.2, 9.6, 13.8 and 19.0. The book's daily mean rose from 0.00045 to 0.0051 across the same quartiles.
- **F4:** No single coin carries the gain. Every coin's book mean is positive (LTC 0.00020 to BTC 0.00128), and the Sharpe with one coin left out stays between 0.61 (without BTC) and 0.82 (without LTC). The book beats holding most clearly on BTC (Sharpe 1.31 vs 0.65).
- **F5:** Much of the edge over holding comes from staying out of falling years. In 2018 the book's daily mean was −0.00019 against the coins' −0.00347, and in 2022 it was −0.00032 against −0.00180, with only 16% of days held in each. In strongly rising years the book lagged holding, for example 2021 at 0.00047 vs 0.00409.
- **F6:** The trade results are right-tailed. The win rate is 45% and the median trade is −0.77%, while the top 10 of 2,401 trades carry 11,493 of the 24,718 summed net percent and the top 5% of trades carry 21,608.
- **F7:** Volatility sizing shifted the gain toward calm periods. The lowest-volatility quartile gave a book mean of 0.00117 on a coin mean of 0.00037, while the highest-volatility quartile gave 0.00060 on a coin mean of 0.00310. Allocation fell from 0.25 to 0.16 between these quartiles.

## Ideas
- `N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation` (from F1, F2, F5): When a coin's 60-day and 20-day returns are both positive, its next few days' returns are higher than its average daily return, so the continuation shows up at a short horizon rather than over the following 20 days.
- `N2-04_slow-and-fast-momentum.e2_stronger-trend-larger-next-day-gain` (from F3, F2, F6): The further a coin's 60-day and 20-day returns sit above their own usual size, the larger its return over the following days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

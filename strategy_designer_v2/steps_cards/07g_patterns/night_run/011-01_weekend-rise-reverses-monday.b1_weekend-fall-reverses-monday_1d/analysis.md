---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3974 USD
---
## Findings
- **F1:** How strongly the next day pushes back against today's volatility-scaled return depends on the coin's 20-day volatility. In a regression of the next day's return on z, volatility rank and their product, the product term has t = -9.3. In the coin's highest 20-day-volatility tercile the slope of the next day's return on z is negative (t = -8.3, n = 5315). In the lowest tercile it is positive (t = +2.7, n = 5315).
- **F2:** In the high-volatility tercile, all of the reversal comes from falls. After down days the slope is -0.0130 (t = -6.7, n = 2610) and the mean next-day return is +0.84%. After up days the slope is +0.0006 (t = +0.37, n = 2716).
- **F3:** The high-volatility reversal holds in every coin: the t runs from -1.9 (XRP) to -5.5 (XMR), with BTC -4.1 and ETH -4.2. It also holds in every year from 2018 to 2024, with t from -1.95 to -4.9 and n from 97 to 1215. It fades only in 2025 (t = +0.29, n = 429).
- **F4:** After a down day, the higher that day's volume relative to its 20-day median, the larger the next day's return (slope 0.0046 per unit of log relative volume, t = +5.4, n = 7906). After an up day the slope is t = +0.95 (n = 8162). Over all days the slope is positive in 7 of 8 years.
- **F5:** The weekend itself shows no specific reversal. For Sunday falls, the slope of the 2-day forward return on z is t = +0.40 (n = 1099). For Sunday rises it is t = +1.50 (n = 1161). Sunday's next-day slope (t = -3.5) is no larger than Saturday's (-5.3) or Wednesday's (-3.5).
- **F6:** The book earns only on Mondays, +0.080% per day, and gives back -0.021% per day on Sundays. It is flat about 59% of the time on those two days and almost always on the other weekdays. So its small Sharpe of 0.32 reflects the general high-volatility fall reversal (F1–F2) more than anything specific to weekends.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal` (from F1, F2, F3, F5): In a coin whose daily volatility over the past 20 days is high, a down day is followed by a rise over the next 1 day. The rise grows with the fall measured in the coin's 20-day daily standard deviations, and the effect strengthens as the coin's 20-day volatility rises.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds` (from F4): After a coin's down day, the higher that day's volume relative to its median daily volume over the past 20 days, the larger the coin's rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

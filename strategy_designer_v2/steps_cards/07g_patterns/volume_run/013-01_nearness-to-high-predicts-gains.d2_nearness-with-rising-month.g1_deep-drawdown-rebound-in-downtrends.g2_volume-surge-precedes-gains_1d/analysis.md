---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3420 USD
---
## Findings
- **F1:** A coin's one-day return predicts its excess 7-day return better than the tested volume forecast. On the non-overlapping 7-day grid, the pooled slope t is 3.45 (n=2299), against 1.96 for the forecast. The slope is positive in all 6 coins (t from 0.07 for LTC to 2.29 for ETH) and positive in 7 of 8 years (2024 is the exception, at t -1.82).
- **F2:** Scaling the one-day return by the coin's 20-day daily volatility keeps the effect (pooled t 3.33, n=2155). Its quintiles rise from -0.0186 / -0.0114 (low / high volume half) in the lowest to +0.0172 / +0.0162 in the highest. The pattern is about the same in both volume halves.
- **F3:** In a joint regression, the volatility-scaled one-day return (t 2.07) and the log volume ratio (t 2.12) each carry their own information, but their product does not (t -0.02). Nearness to the 20-day high adds little once both are in (t 1.30, n=2155).
- **F4:** The volume effect sits at the thin end, not in bursts. In the lowest volume-ratio quintile, the excess 7-day return is -0.0194 (t -3.32, n=432). The other quintiles range from -0.0059 to +0.0089 and none reaches |t| 1.5. The highest quintile is only +0.0035 (t 0.47).
- **F5:** Thin volume is followed by weakness whichever way the day closed. After thin-volume down days the excess return is -0.0242 (t -2.97, n=201), and after thin-volume up days it is -0.0152 (t -1.83, n=231). After non-thin up days it is +0.0107 (t 2.32, n=915).
- **F6:** The book's daily returns largely follow the coin. In its worst book-return decile the coin fell -0.068 that day, and in its best decile the coin rose +0.075. The long-only book's mean daily return of 0.00074 is below holding's coin-day mean of about 0.0012, which fits its failed Calmar of 0.41.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.g1_volatility-scaled-daily-move-continues` (from F1, F2, F3): The larger a coin's one-day return relative to its own 20-day daily volatility, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains.g2_thin-volume-precedes-weakness` (from F3, F4, F5): The thinner a coin's traded volume over the past day relative to its 20-day average, the lower its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

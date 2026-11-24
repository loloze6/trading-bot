---
line: 7.g patterns
backtest: 031-03_fading-volume-after-rise-reverses_1d
idea tested: 031-03_fading-volume-after-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3786 USD
---
## Findings
- **F1:** Across all six coins on the non-overlapping 14-day grid (700 cases, 131 days), the log of the last 14 days' mean volume over the last 30 days' mean volume predicts the next 14 days' excess return with a positive sign: the day-clustered t is 2.59. Its quintiles run from -4.86 % (volume fallen most, log ratio -0.41) to +4.62 % (volume risen most, +0.32), a spread of about 9.5 % against a cost of 0.19 % per trade.
- **F2:** The F1 volume effect holds whether the past 14-day return was up (t 2.91, 197 cases) or down (t 3.01, 189 cases). It is positive on every coin, with t from 0.79 (XMR) to 2.31 (LTC), and in 7 of 8 years, at t 2.41 in 2023 and 3.14 in 2024 (2019 at -0.33). Controlling for the past 14-day return leaves it at t 4.01, while the past return itself drops to t -0.25.
- **F3:** The same volume ratio shows no effect over 30 days (t -0.18, 386 cases), but it shows one over 7 days (day-clustered t 1.81, 1,678 cases). The effect lives at one to two weeks, not at the tested 30-day horizon.
- **F4:** The brief's reversal does not appear at two months: the 60-day past return regressed on the next 30 days' excess return gives slope -0.0126 with t -1.00 (246 cases). Shorter past returns lean toward continuation, not reversal: the 7-day past return predicts the next 7 days with a day-clustered t of 2.22 (1,678 cases), though it is mixed by year (2018 at -0.17, 2023 at -0.46) and absent at 14 days (t 0.38).
- **F5:** The book's shorts on rising coins lost heavily. The mean net trade was -23.0 % on ETH (37 trades), -19.6 % on LTC, -16.8 % on ZEC and -30.9 % on XRP. Only BTC (+6.6 %) and XMR (+0.07 %) did not lose.
- **F6:** Saturdays rose more than other days: the coins' mean daily return per day was +0.47 % (t 3.14, 414 days), positive in 6 of 8 years and near 0 in 2022 and 2023. It is one weekday picked from seven and has no grade, so it gives no idea.

## Ideas
- `031-03.g1_volume-surge-leads-two-week-drift` (from F1, F2, F3, F5): The more a coin's mean daily volume over the last 14 days has risen above its mean daily volume over the last 30 days, the more its price rises over the next 14 days; the more that volume has fallen below its 30-day mean, the more its price falls over the next 14 days.
- `031-03.g2_one-week-momentum-continues` (from F4, F5): The larger a coin's 7-day return relative to its usual 7-day move over the past 30 days, the more its price keeps moving the same way over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3660 USD
---
## Findings
- **F1:** A coin's 1-day return predicts its next 1-day return with the opposite sign, and only when its volatility is high. On the non-overlapping daily grid, the slope of the excess next-day return on the 1-day return is -0.1367 (t -11.09, n 5511) in each coin's top tercile of 7-day volatility. It is +0.0372 (t 2.13, n 5508) in the bottom tercile and +0.0157 (t 1.09, n 5507) in the middle one.
- **F2:** The 1-day reversal holds in every coin and almost every year. Pooled over all bars it is a slope of -0.0836 (t -10.97, n 17102). By coin, the slope runs from -0.064 (XRP, t -3.43) to -0.129 (XMR, t -6.93). By year, 7 of 8 slopes are negative, with t from -1.73 to -7.69; 2024 is the exception at +0.0075 (t 0.35).
- **F3:** The reversal shows mostly as a rebound after the worst days. In the bottom quintile of the 1-day return scaled by volatility, the next day's excess return is +0.41% (t 4.19, n 3306). The top quintile is -0.21% (t -2.39) and the middle quintiles sit near -0.1%.
- **F4:** The tested 7-day momentum does not appear in four of the six coins on their own. While the 30-day return is positive, the slope of the excess 7-day forward return on the 7-day return pooled is 0.134 (t 4.05, n 871). It comes from XRP (t 2.51) and ZEC (t 2.38); BTC, ETH, LTC and XMR all have t below 0.6, with about 150 cases each.
- **F5:** The idea does not explain a strong hour-of-day effect in the bars. Hourly returns at 21:00–22:59 UTC average +0.050%/bar against roughly +0.002% at other hours (Welch t 8.16). This holds in every coin (t 3.0–4.6) and in 7 of 8 years. The book's hourly gain in those two hours is 0.000128 (t 6.50), against 0.000028 at other hours.
- **F6:** Saturdays are the coins' best day. Saturday daily returns average +0.454% (t 5.53, n 2484), positive in every coin (t 1.40–2.92) and in 6 of 8 years. The book's Saturday mean return of 0.00162 (t 4.16) is its best weekday.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum.g1_high-volatility-daily-reversal` (from F1, F2, F3): The more a coin has fallen over the past 1 day, the higher its return over the next 1 day. The effect grows the higher the coin's 7-day volatility, and the largest rebounds follow the steepest falls when volatility is high.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum.g2_volatility-spike-sharpens-reversal` (from F1, F2): The higher a coin's 7-day volatility relative to its 30-day volatility, the larger the reversal of its 1-day return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

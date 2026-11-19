---
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
idea tested: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3880 USD
---
## Findings
- **F1:** The rebound after a fall in the last day is concentrated in the first one to two days and largely spent by day three. When the coin is down over 72 bars, the slope of forward excess return on the standardised 24h move is -0.0019 (t -12.4, n 33184) at 6h, -0.0084 (t -14.2, n 8272) at 24h, -0.0117 (t -10.4, n 4040) at 48h and -0.0069 (t -4.07, n 2669) at 72h, and the verdict's 24-to-72-bar slope is only 6.0e-05.
- **F2:** The reversal needs a falling 3-day backdrop; when the coin is up over 72 bars, the 24h reversal slope is -0.0022 (t -3.8, n 8542) and the 48h slope is -0.0009 (t -0.76, n 4251).
- **F3:** Measured unconditionally on a 24h grid, the lowest quintile of 24h move is followed by +0.48% excess over the next 24h (t 4.59, n 3308), and the highest quintile by -0.32% (t -3.24, n 3305).
- **F4:** The level of recent volatility decides the sign of the effect: in the top tercile of 24h hourly volatility the 24h slope on the past 24h move is -0.0058 (t -10.1, n 5607), while in the bottom tercile it is +0.0027 (t 2.17) at 24h and +0.0127 (t 3.13, n 1846) at 72h; by volatility quintile, the next-day move in the past move's direction is -0.60% (t -4.55) in the top quintile against +0.03% (t 0.50) in the bottom.
- **F5:** How a large move was built does not change its next-day reversal, contrary to the brief: across terciles of path efficiency the move-signed next-24h excess is -0.25%, -0.47% and -0.23%; across terciles of largest-hour share it is -0.42%, -0.28% and -0.25%; and across terciles of volume concentration it is -0.41%, -0.22% and -0.32%.
- **F6:** The book fails because hourly re-sizing churns a signal whose edge lives at the daily scale. The mean gross gain per bar is 4e-06 (t 0.70) on turnover of 0.046 of the book per bar. Over 58401 trades with a median length of 5 hours, the mean return is -0.39% before fees and -0.49% after, and the mean daily book return is negative in every year from 2018 to 2025.
- **F7:** The hours starting 21:00 and 22:00 UTC carry positive excess hourly returns (t 6.09 and 4.95, about 17400 bars each), with t between 2.6 and 4.0 in every one of the six coins and positive in 7 of 8 years (2022: t -1.87). The hours 03:00 UTC (t -4.74) and 14:00 UTC (t -4.44) are negative.

## Ideas
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g1_one-day-fresh-drop-rebound` (from F1, F2, F3, F6): When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 1 day.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g2_volatility-graded-daily-reversal` (from F4, F3): The more volatile a coin's hourly returns have been over the past 1 day, the more its 1-day move reverses over the next 1 day.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.g3_calm-day-move-continuation` (from F4): When a coin's hourly returns over the past 1 day have been calm, the larger its 1-day move, the more it keeps moving the same way over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

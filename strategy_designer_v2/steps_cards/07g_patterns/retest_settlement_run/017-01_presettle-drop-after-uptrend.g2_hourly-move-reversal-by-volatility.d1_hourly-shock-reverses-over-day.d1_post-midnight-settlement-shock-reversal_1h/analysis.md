---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4123 USD
---
## Findings
- **F1:** The 24-hour reversal after a volatility-scaled hourly move is specific to the hour starting 00:00 UTC. At that hour the slope t is 7.84 and moves of at least one usual hourly move give +0.50 % signed (t 7.19, 5762 cases). Pooled over all other hours, the slope t is 0.59 and the signed mean is +0.014 % (t 0.89, 101012 cases). No other hour reaches a signed mean above 0.29 %.
- **F2:** The hour-0 reversal is about twice as large on Saturday and Sunday. Weekend days give +0.82 % (t 6.76, 1572 cases) against +0.38 % (t 4.52, 4190 cases) on Monday to Friday, a Welch t of 2.98. Saturday alone gives +0.94 % (t 4.98) and Tuesday gives -0.06 % (t -0.29).
- **F3:** The weekend lift holds in every volatility tercile, and it is largest when the coin's 24-hour volatility is high against its 30-day volatility. Weekend hour-0 moves give +0.60 % (t 3.59) in low volatility, +0.42 % (t 1.81) in mid and +1.32 % (t 4.24) in high. On weekdays the same terciles give +0.005 % (t 0.03), +0.28 % and +0.39 %.
- **F4:** Across the other 23 hours, the regime set by recent volatility decides the 24-hour direction. Where 24-hour volatility is high against 30-day volatility, hourly moves of 1 to 2 usual moves reverse by +0.22 % (t 5.06, 17453 cases) and moves above 3 by +0.35 % (t 2.32). Where it is low, moves of 2 to 3 continue by -0.18 % (t -2.79) and moves above 3 by -0.43 % (t -3.10, 951 cases).
- **F5:** The hour-0 reversal partly gives itself back on the following day. For hour-0 moves of 2 to 3 usual moves, the second day's signed return is -0.53 % (t -3.21, 1012 cases) after +0.67 % on the first day. The 48-hour signed mean is only +0.16 % (t 0.67).
- **F6:** The book loses on the days the coins move most. On the fifth of days with the largest absolute coin return its mean daily return is -0.29 % (std 3.27 %), against +0.20 % to +0.23 % on the two calmest fifths. This day-level drag is what keeps Calmar at 0.47.
- **F7:** The hour-0 effect weakened in 2023 and 2024. Its signed mean on large moves was +0.15 % (t 1.26) and +0.17 % (t 0.93), against +0.47 % to +0.88 % in 2018 to 2021 and 2025. The book's Sharpe in those two years was -0.15 and 0.12.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal` (from F2, F3, F1): The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement on a Saturday or Sunday, relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way. This weekend reversal is larger than the weekday one.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal` (from F4, F3): When a coin's 24-hour volatility is high relative to its 30-day volatility, the larger its 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way, at any hour of the day.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation` (from F4): When a coin's 24-hour volatility is low relative to its 30-day volatility, the larger its 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours continues in the same direction.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade` (from F5): The larger the coin's 24-hour return after the first hour following the 00:00 UTC settlement runs against that hour's move, the more its return over the following 24 hours runs back toward that hour's direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

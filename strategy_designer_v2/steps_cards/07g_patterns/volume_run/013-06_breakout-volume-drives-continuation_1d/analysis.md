---
line: 7.g patterns
backtest: 013-06_breakout-volume-drives-continuation_1d
idea tested: 013-06_breakout-volume-drives-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3370 USD
---
## Findings
- **F1:** On all bars (one-day non-overlapping grid, coin-demeaned), a day's volume relative to its 30-day average predicts the next day's return only after down days: on down days the top volume quintile minus the bottom quintile is +0.0093, Welch t 4.89, with 7086 cases; on up days it is +0.0001, t 0.06, with 7257 cases.
- **F2:** The relative-volume effect on the next day keeps its sign across coins and years. The top-minus-bottom quintile is positive in all 6 coins, from +0.0015 for XMR to +0.0091 for ZEC (ZEC t 2.39). It is positive in all 8 years, from +0.0001 to +0.0099, with t 2.35 in 2021 and t 2.56 in 2024. The pooled quintile spread is +0.0046 (q4 +0.0031 against q0 -0.0015), Welch t 3.53, with 14343 cases.
- **F3:** A day's return scaled by its 20-day volatility predicts a next-day reversal. The bottom quintile (the largest falls) is followed by +0.0040 and the top quintile by -0.0010, Welch t -3.83 with 14907 cases. The effect sits on heavy-volume days (hi-minus-lo -0.0061, t -2.91) and is absent on light-volume days (-0.0003, t -0.20). In a joint regression it stays at t -3.74 next to log relative volume at t +4.13.
- **F4:** The reversal after scaled one-day moves is negative in 5 of 6 coins on the next day (XMR -0.0098, t -3.45), and its rank correlation is negative in every coin, from -0.033 to -0.104. By year it is strongest in 2018, 2020 and 2023 (t -2.76, -2.92, -3.23) and fades in 2024 and 2025 (t +1.02, +0.86).
- **F5:** The tested breakout book is in a position on only 2.6% of bars (441 bars), earning 0.0066 per in-position bar. It barely follows the market: its mean daily return by year is between -0.00003 and 0.00056, while the coins' is between -0.0035 and 0.0042. Its trades last a median of 1 to 2 days.
- **F6:** The next-day return by weekday shows Friday at +0.0030 (t 3.66) and Wednesday at -0.0030 (t -2.75). These are 7 tests among many angles and there is no mechanism behind them, so this is weaker than F1 to F3.

## Ideas
- `013-06_breakout-volume-drives-continuation.g1_heavy-volume-selloff-next-day-rebound` (from F1, F2, F3): When a coin closes down on a day, the heavier that day's volume relative to its own 30-day average volume, the larger the coin's rise over the next 1 day.
- `013-06_breakout-volume-drives-continuation.g2_volatility-scaled-fall-reverses` (from F3, F4, F1): The larger a coin's one-day fall measured against its own 20-day daily volatility, on a day whose volume is above its 30-day average, the larger its rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

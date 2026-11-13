---
line: 7.g patterns
backtest: N2-05_shock-up-continuation_1d
idea tested: N2-05_shock-up-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3364 USD
---
## Findings
- **F1:** After big up days the drift builds beyond the plan's 5-bar horizon. For days of 2 to 3 times the trailing 20-day mean absolute return, the 10-bar excess return is +3.61% (t 3.52, 445 de-duplicated events) against +1.36% at 5 bars (t 2.31). For days above 3 times, it is +3.12% at 10 bars (t 2.64, 334 events) against +0.83% at 5 bars (t 1.24). Events are merged within 5 bars, so the 10-bar windows can overlap partly.
- **F2:** Very large down days, below -3 times the trailing scale, are followed by a further 5-bar excess return of -1.35% (t -2.18, 252 de-duplicated events). Down days between -3 and -2 show no such continuation (+0.53%, t 1.09, 419 events).
- **F3:** Moderate down days, between -2 and -1 times the trailing scale, are followed by a next-day excess return of +0.60% (t 4.10, 1020 de-duplicated events). Flat days (-1 to 1) show -0.11% (t -1.09, 2004 events).
- **F4:** The next-day excess return depends on the weekday of the signal bar. After a Friday close it is +0.30% (t 3.76, 2479 coin-days) and after a Thursday close +0.25% (t 2.63, 2483). After a Monday close it is -0.24% (t -2.53, 2490) and after a Wednesday close -0.30% (t -2.70, 2489). These coin-days are pooled over six coins that move together, so the effective count is smaller.
- **F5:** When a coin's 20-day volatility is below 0.8 times its 120-day median and its 20-day return is positive, the next non-overlapping 5-bar excess return is +3.01% (t 2.48, 128 cases). Low volatility with a negative 20-day return gives -0.89% (t -1.03, 156 cases). Mid volatility gives +0.32% with a positive 20-day return and -0.80% with a negative one.
- **F6:** Big up days (≥2 times the scale) continue when the coin's 20-day return is already positive: +1.34% over 5 bars (t 2.21, 468 events), against +0.39% (t 0.65, 256 events) when it is negative.
- **F7:** The continuation after big up days comes from a few years and coins. It is +4.72% in 2021 (t 2.93, 86 events) and +3.75% in 2024 (t 2.63, 84 events), but negative in 2022 (-1.46%, t -1.07) and 2023 (-0.93%, t -1.39). Among coins, ZEC carries most of it (+3.51%, t 2.22, 115 events), while BTC and ETH sit near zero (t 0.20 and -0.01).
- **F8:** The book's losses come from one-day trades. Trades lasting up to 1.5 days number 1730 and average -1.11% net. Trades lasting 1.5 to 3.5 days (328) average +7.74%, and trades lasting 3.5 to 10 days (292) average +8.77%. The book still has a Sharpe of -0.24 overall.

## Ideas
- `N2-05_shock-up-continuation.g1_slow-building-shock-drift` (from F1, F8): After a coin closes up by more than about twice its trailing 20-day mean absolute daily return, its price keeps drifting up over the following two weeks, more than over the first five days.
- `N2-05_shock-up-continuation.g2_shock-continuation-within-uptrend` (from F6, F1): A big up day continues upward over the following days when the coin's close is already above its close of 20 bars earlier.
- `N2-05_shock-up-continuation.g3_extreme-down-day-continuation` (from F2): After a coin closes down by more than about three times its trailing 20-day mean absolute daily return, its price keeps falling over the next five days.
- `N2-05_shock-up-continuation.g4_moderate-dip-next-day-rebound` (from F3): After a coin closes down by between one and two times its trailing 20-day mean absolute daily return, it rises the next day.
- `N2-05_shock-up-continuation.g5_friday-close-to-saturday-drift` (from F4): A coin's close-to-close return from Friday's UTC close to Saturday's UTC close is positive on average.
- `N2-05_shock-up-continuation.g6_calm-uptrend-upward-drift` (from F5): When a coin's 20-day volatility is low against its own recent history and its 20-day return is positive, it drifts up over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

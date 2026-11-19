---
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
idea tested: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4044 USD
---
## Findings
- **F1:** The coin's 1-day return reverses over the next day, and this holds in every coin. On the non-overlapping 24-hour grid, the Spearman correlation of the 1-day return with the next day's excess return is negative in all six coins, from rho -0.052 (ZEC, t -2.67, n 2664) to rho -0.117 (XRP, t -6.22, n 2774).
- **F2:** The 1-day reversal is negative in every year: rho runs from -0.124 (2018, t -5.65) through -0.112 (2023, t -5.11) to -0.052 (2024, t -2.36) and -0.032 (2025, t -1.44). It weakens in the most recent years.
- **F3:** Most of the reversal comes from falls. When the 1-day return is scaled by the coin's own 3-day hourly volatility (rho -0.073, t -9.46, n 16526), the bottom quintile gains +0.42% excess over the next day (t 4.36, n 3306). The top two quintiles lose only about -0.18% (t -2.23 and -2.04).
- **F4:** The brief's grind-versus-jump angle does not hold up across coins or years. The efficiency of the 3-day path (net move over the sum of absolute hourly moves) against the next 3 days' sign-aligned excess return has t between -1.08 and 1.56 in every coin, and between -1.26 and 1.50 in every year. The jump share (rho -0.018, t -1.32) and the volume concentration (rho 0.013, t 0.93) show nothing in pooled data.
- **F5:** The book is mostly the coins' own move done worse. Its daily returns correlate 0.76 with holding the coins. Its Sharpe is 0.087 against holding's 0.554. In all six coins its mean daily return (-0.00018 to +0.00036) is far below the coin's own (0.00067 to 0.00155).
- **F6:** The tested 3-day signal is the weaker horizon. Within 3-day declines the 3-day return predicts the next 3 days' excess return at only rho -0.061 (t -3.17, n 2669), and no single coin reaches t -2.1 (from BTC -0.36 to XRP -2.06). The 1-day horizon in F1 is significant in every coin.
- **F7:** Hourly returns from 21:00 to 23:00 UTC average +4.3 to +5.6 bp in every coin (t 3.0 to 4.6). The drift is positive on all seven weekdays and in seven of eight years (2022: -2.2 bp, t -1.46). Because it is a time-of-day condition and not a graded situation, I do not turn it into an idea.

## Ideas
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g1_one-day-fall-next-day-rebound` (from F1, F2, F3, F6): The larger a coin's fall over the last 1 day, measured against its own hourly volatility over the past 3 days, the more it rises over the next 1 day.
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.g2_one-day-rise-next-day-giveback` (from F1, F2, F3): The larger a coin's rise over the last 1 day, measured against its own hourly volatility over the past 3 days, the more it falls back over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

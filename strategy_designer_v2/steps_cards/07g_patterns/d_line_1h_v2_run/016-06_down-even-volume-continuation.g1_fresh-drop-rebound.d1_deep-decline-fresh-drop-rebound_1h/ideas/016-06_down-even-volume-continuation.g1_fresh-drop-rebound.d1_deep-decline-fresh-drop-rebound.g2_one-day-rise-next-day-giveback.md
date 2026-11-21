---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's rise over the last 1 day, measured against its own hourly volatility over the past 3 days, the more it falls back over the next 1 day.
Consequence: Trim or refuse longs after sharp one-day rallies, in proportion to their volatility-scaled size, over the following day.
Why:
- F1: The coin's 1-day return reverses over the next day, and this holds in every coin. On the non-overlapping 24-hour grid, the Spearman correlation of the 1-day return with the next day's excess return is negative in all six coins, from rho -0.052 (ZEC, t -2.67, n 2664) to rho -0.117 (XRP, t -6.22, n 2774).
- F2: The 1-day reversal is negative in every year: rho runs from -0.124 (2018, t -5.65) through -0.112 (2023, t -5.11) to -0.052 (2024, t -2.36) and -0.032 (2025, t -1.44). It weakens in the most recent years.
- F3: Most of the reversal comes from falls. When the 1-day return is scaled by the coin's own 3-day hourly volatility (rho -0.073, t -9.46, n 16526), the bottom quintile gains +0.42% excess over the next day (t 4.36, n 3306). The top two quintiles lose only about -0.18% (t -2.23 and -2.04).

---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its typical daily move over the past 20 days, the higher that coin's return over the next 1 day.
Consequence: A trader can buy a coin at the close of an unusually sharp down day, more the sharper the fall, and expect a rebound of several times the cost of a trade the next day.
Why:
- F1: A coin's next-day return after a large one-day fall, measured against its prior 20-day volatility, is clearly above normal. In the bottom two of twenty groups the next-day excess return is +0.50 % (t 2.25, n 755) and +0.61 % (t 3.19, n 754). Across all bars the Spearman correlation between the scaled one-day return and the next day's excess return is −0.078 (p 1e-21, n 15076).
- F2: The reversal is graded inside the bottom 10 % of scaled one-day returns: the slope of next-day excess return on the scaled return is −0.00463 (t −3.59, n 1509), so the deeper the fall, the larger the rebound.
- F3: The rebound after the bottom 10 % of scaled falls holds in both 20-day regimes, at +0.57 % after a 20-day fall (t 3.02, n 1025) and +0.52 % after a 20-day rise (t 2.38, n 484). It is positive in 0.75 of the 24 windows and in all six coins, from +0.26 % for BTC (t 0.95) to +1.02 % for XMR (t 2.92).
- F4: The rebound is uneven over the years: +0.82 % in 2018 (t 1.93), +1.52 % in 2020 (t 2.89) and +1.81 % in 2021 (t 3.34), but about zero in 2019, 2022, 2024 and 2025 (from −0.06 % to +0.06 %). Its per-case size, about 0.5–0.6 %, is roughly three times the 0.19 % cost of a trade.

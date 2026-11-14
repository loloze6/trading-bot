---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.f real and profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin's daily bars, after a close at its highest close of the prior 20 days, the next day's rise is larger while the close stays above its close of 20 bars earlier and the coin's 20-day volatility is in its upper third.
Consequence: A trader would hold a breakout long only while the coin stays above its level of 20 days before, and would favour volatile stretches over calm ones.
Why:
- F3: The book earns only when the coin is above its close of 20 days earlier. Next-day book return there averages 0.0037 (7187 days, sum 26.7), against -0.0001 when it is below (7313 days, sum -0.82). The best cell is rising and volatile (mean 0.0061, 2256 days); the worst is falling and calm (mean -0.0013, 2408 days).
- F2: The gain depends on a few rising years and moves with plain holding. Trade net sums are -4728 in 2018 and -2121 in 2022. Book Sharpe falls from 0.57 overall to 0.32 without 2020 and to 0.03 without 2020, 2024 and 2025. Yearly book Sharpe tracks holding's (2018: -1.23 vs -1.10; 2022: -0.56 vs -0.76; 2020: 2.15 vs 1.52).

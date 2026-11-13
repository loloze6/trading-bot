---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.g patterns
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A big up day continues upward over the following days when the coin's close is already above its close of 20 bars earlier.
Consequence: A trader should take big up-day signals only when the coin is already up over the past 20 days.
Why:
- F6: Big up days (≥2 times the scale) continue when the coin's 20-day return is already positive: +1.34% over 5 bars (t 2.21, 468 events), against +0.39% (t 0.65, 256 events) when it is negative.
- F1: After big up days the drift builds beyond the plan's 5-bar horizon. For days of 2 to 3 times the trailing 20-day mean absolute return, the 10-bar excess return is +3.61% (t 3.52, 445 de-duplicated events) against +1.36% at 5 bars (t 2.31). For days above 3 times, it is +3.12% at 10 bars (t 2.64, 334 events) against +0.83% at 5 bars (t 1.24). Events are merged within 5 bars, so the 10-bar windows can overlap partly.

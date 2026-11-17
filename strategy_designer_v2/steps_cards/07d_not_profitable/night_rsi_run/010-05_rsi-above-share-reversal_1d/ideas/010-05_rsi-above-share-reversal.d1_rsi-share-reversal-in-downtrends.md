---
brief: 010_rsi-midline-regime-direction
source-idea: 010-05_rsi-above-share-reversal
line: 7.d not profitable
backtest: 010-05_rsi-above-share-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent above 50, the lower the coin's return over the next 14 days, only while the coin's 90-day return is negative.
Consequence: A trader should bet on reversal of RSI dominance only in coins that have been falling over three months, and refuse those shorts in rising coins.
Why:
- F2: The losses sit where the coin had risen over the past 30 days. There the book was short on 1775 bar-days and lost -0.002498 a day while the coin gained +0.003101 a day. Where the 30-day return was negative, shorts gained +0.000490 over 388 bar-days.
- F3: Sorted by 90-day trend, the book was most short in the rising tercile (mean position -0.73) and lost -0.001914 a day there. In the falling tercile it was net long (mean position +0.47) and earned +0.000961 a day. The coin's next-day return was +0.001707 in the rising tercile and +0.002393 in the falling one.
- F4: On the non-overlapping 14-day grid, the RSI-above-50 share does not predict reversal overall: slope +0.005, t 0.15, n 192. Its sign splits by trend. Where the 30-day return was positive the slope was +0.079 (t 1.33, n 109), meaning continuation. Where the 30-day return was non-positive it was -0.102 (t -1.42, n 83), meaning reversal. In the rising 90-day tercile the slope was +0.256 (t 2.43, n 18).
- F6: Zeroing the shorts taken after a positive 30-day return lifts the daily book from mean -0.001202 (Sharpe -0.96) to -0.000193 (Sharpe -0.22). The book is still below zero, so removing the shorts in rises closes most of the gap but does not by itself make it pay.

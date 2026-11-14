---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the first 20 bars after a coin's 50-day SMA crosses below its 200-day SMA, the price rises over the next 10 bars.
Consequence: A trader would treat a fresh death cross as an exhausted down-move and stay long, or buy it, instead of exiting.
Why:
- F2: The drift does not start at the cross. In the first 20 bars after the 50-day SMA rises above the 200-day, the forward 10-bar return is -1.03%; at 20 to 60 bars of age it is +2.97%. In the first 20 bars after a down-cross, while the book is flat, it is +2.09%. Moves right after a cross reverse.
- F1: The book is long-only and earns less than holding (Sharpe 0.376, which is 0.193 below holding's), because the coin keeps rising while the book is flat: next-day coin return is +0.089% on flat bars against +0.157% on active bars, flat bars make up 42% of all bars, and in 2020, 2023 and 2024 flat bars rose more than active bars (+0.71% vs +0.30%, +0.28% vs +0.06%, +0.40% vs +0.18% per day).

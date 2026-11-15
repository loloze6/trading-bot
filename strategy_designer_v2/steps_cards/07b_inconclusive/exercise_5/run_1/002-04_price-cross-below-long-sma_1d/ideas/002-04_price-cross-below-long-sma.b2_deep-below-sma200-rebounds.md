---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is far below its 200-day simple moving average and that average has stopped falling over the past 50 days, the deeper the close sits under the average, the more the coin rises beyond its average over the next 10 days.
Consequence: A trader would refuse to short deep, stalled declines and would treat them as rebound candidates.
Why:
- F1: The short excess return sits only in the shallow half of the below-average bars, where the close is just under its 200-day SMA: over 10 days, shallow blocks give mean excess -0.0118 (t -1.91, n 420) against +0.0049 in deep blocks (t 0.66, n 421), a shallow-minus-deep Welch t of -1.72. The plan's forecast sizes the short larger the deeper the close sits, which points the opposite way and explains its negative slope of -0.0126 and pooled t of -0.23.
- F4: Deep-below bars reverse upward in some years and some states. Deep 10-day excess is +0.109 (t 4.74) in 2020, +0.116 (t 2.70) in 2021 and +0.064 (t 2.27) in 2024. It is also +0.038 (t 1.81) when the 50-day SMA slope is flat or rising, while deep in low volatility falls (-0.032, t -2.02). This mixes downward persistence with rebounds.

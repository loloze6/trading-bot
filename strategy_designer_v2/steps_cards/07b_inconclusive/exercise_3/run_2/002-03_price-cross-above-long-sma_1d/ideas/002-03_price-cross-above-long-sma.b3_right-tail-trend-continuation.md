---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits above its 200-day simple moving average, its rises over the following weeks are larger than its falls, the more so the further above the average it sits.
Consequence: A trader would expect such a long to lose small most of the time and earn through rare large runs, and would size and judge it on its payoff ratio rather than its hit rate.
Why:
- F2: The plan's block t of 1.73 rests on a handful of blocks. The top 10 of 811 blocks sum to 132.7, more than the 102.4 total, while the bottom 10 sum to −41.5. Only 16–27% of each coin's blocks are positive. The effect therefore shows as rare large continuations, not frequent ones.
- F1: Bar by bar the effect is close to zero. On the non-overlapping 20-bar grid, bars with forecast > 0 beat the coin's pooled mean by 0.0052 (t 0.32, n 399), against −0.00015 (t −0.01, n 412) for bars below the SMA. Only 40.6% of them win, and the median is −0.036. No horizon from 5 to 60 bars gets past |t| 0.61.
- F4: Only the largest standardised forecasts carry a gain. The top forecast quartile gives +0.072 (t 1.34, n 100) and the bottom quartile −0.035 (t −1.81, n 100), with the middle two near zero (−0.004, −0.013). Raw-distance sextiles show no order (+0.0125 and +0.0128 for the two highest, −0.015 just above the SMA).

---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 50-day SMA is above its 200-day SMA but whose close has fallen below its 50-day SMA, the close 10 days later is lower relative to the current close than the coin's typical 10-day move.
Consequence: A trader would refuse or cut longs in a golden-cross regime once price has slipped below the 50-day average.
Why:
- F2: Inside the active state (50-day SMA above 200-day), the past 20-day return splits the outcome: when it is positive the next 10 bars beat the coin's mean by +2.14% (n=361, t=2.00), and when it is negative they fall short by -1.78% (n=333, t=-2.36). With the same split on flat bars the results are -0.47% and -0.07% (|t|≤0.65).
- F4: Active bars where the close is below its 50-day SMA are followed by -3.23% excess over 10 bars (n=205, t=-3.62), versus +0.68% (n=288, t=0.62) when the close is above it. The past 10-day sign gives the same split: -1.87% (t=-2.38) when down and +2.35% (t=2.22) when up.

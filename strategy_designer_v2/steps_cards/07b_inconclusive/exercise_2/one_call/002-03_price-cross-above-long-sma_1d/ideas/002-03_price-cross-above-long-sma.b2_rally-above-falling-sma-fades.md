---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits well above its 200-day SMA while that SMA has fallen over the last 20 bars, the coin's return over the next 20 bars falls short of its own average 20-bar return.
Consequence: A trader would refuse longs on rallies above a still-falling long average, because these behave like bear-market bounces that fade.
Why:
- F2: The effect splits by the direction of the 200-day SMA's own 20-bar slope combined with forecast strength. With the SMA rising and the forecast above 10, the mean excess is +0.074 (t 1.77, n 131, hit 44%). With the SMA falling and the forecast above 10, it is -0.058 (t -2.05, n 57, hit 35%). The weak-forecast cells are both about -0.02 (t -0.91 and -1.21).
- F4: The fresh cross does not lead to persistence. Active samples within 20 bars of the upward cross average -0.021 (t -1.21, n 162). Samples 20 to 60 bars after the cross average +0.026 (t 0.74, n 151).

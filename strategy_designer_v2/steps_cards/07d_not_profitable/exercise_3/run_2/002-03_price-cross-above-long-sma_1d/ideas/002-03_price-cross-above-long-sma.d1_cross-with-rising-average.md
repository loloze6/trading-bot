---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its long moving average, it keeps drifting upward further the further it sits above, only while the long moving average itself is rising, and the drift grows with the steepness of that rise.
Consequence: A trader stays long above the average only while the average is climbing, and sizes up with its slope, which removes the flat-average losses that drag the book below holding.
Why:
- F1: The book loses on the days it holds a coin above a flat or falling 200-day SMA. Held days with the SMA's 20-day slope between -5% and 0 averaged -0.000144 (n=1460, t -0.13), and slope at or below -5% averaged 0.000556 (n=172, t 0.27). With a rising SMA the held days averaged 0.001715 (n=3655, t 2.04) for slope 0 to 5% and 0.004502 (n=2300, t 2.69) for 5 to 15%.
- F2: On non-overlapping 20-bar blocks, active bars with a non-positive SMA slope had a 20-bar excess return of -0.033 (n=64, t -1.46). Active bars with a positive slope had +0.034, +0.019 and +0.014 across the three slope bands (n=139, 100, 27). On daily bars, keeping only the positive-slope days raised the Sharpe from 0.394 to 0.509, level with holding at 0.509.
- F6: The falls sit in a few windows. The book lost -0.33, -0.39 and -0.48 in w12, w13 and w18 against the coins' -0.15, -0.31 and -0.24, while w24 (4.37) and w11 (2.06) carry the gain. XMR's book Sharpe was -0.02 against 0.48 for holding it, with a deepest fall of -0.96.

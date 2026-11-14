---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits far above its 200-day SMA, at the top of its own recent range of distances, the coin keeps rising over the next 20 bars more than its usual drift.
Consequence: Take the long only when the distance above the long average is extreme for that coin, and not on a mere close above it.
Why:
- F3: The effect sits in the largest forecasts only: the top forecast quintile (close about 88% above the 200-day SMA, forecast near the 20 cap) has mean excess +0.052, against -0.027 and -0.023 in the two lowest quintiles; blocks in the lowest third of mean forecast lose -0.18 with t -5.09, while the highest third gain +1.27 with t 1.70.
- F4: Measured against the cross-coin average 20-bar return, the forecast adds nothing overall (relative return -0.001 when on vs +0.001 when off); only the top quintile beats the other coins (+0.039 mean, 49.0% hit), while quintiles 0 to 3 all trail them (-0.007 to -0.016).

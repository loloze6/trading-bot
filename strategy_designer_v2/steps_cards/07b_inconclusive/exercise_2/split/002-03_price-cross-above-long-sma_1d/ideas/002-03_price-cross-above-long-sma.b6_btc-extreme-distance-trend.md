---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When BTC's close is far above its 200-day SMA, at the top of its own recent range of distances, BTC keeps rising over the next 20 bars more than its usual drift on most such bars.
Consequence: Apply the extreme-distance long to BTC, where the edge is broad and not reliant on rare outliers.
Why:
- F5: In the top forecast quintile the result splits by coin: BTC is the only coin with a clean edge (mean +0.063, median +0.027, 58.5% hit); ZEC's +0.215 mean rests on tails (median -0.026); XRP (23.8% hit, median -0.129) and XMR (32.7% hit, mean -0.040) lose.
- F3: The effect sits in the largest forecasts only: the top forecast quintile (close about 88% above the 200-day SMA, forecast near the 20 cap) has mean excess +0.052, against -0.027 and -0.023 in the two lowest quintiles; blocks in the lowest third of mean forecast lose -0.18 with t -5.09, while the highest third gain +1.27 with t 1.70.

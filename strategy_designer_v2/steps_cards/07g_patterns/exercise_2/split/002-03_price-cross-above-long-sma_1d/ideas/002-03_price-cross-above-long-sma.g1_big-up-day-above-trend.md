---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits above its 200-day SMA and the day's return is an up-move larger than 2 standard deviations of its recent daily returns, the coin keeps rising over the next 5 bars, further than after ordinary days above the SMA.
Consequence: A trader would add or open a long after a large up-day only while the coin is above its long average, and not on large up-days below it.
Why:
- F1: When the close was above the 200-day SMA, a daily up-move larger than 2 standard deviations was followed by a mean 5-bar return of +3.39% (t=3.81, n=323, overlapping windows). Below the SMA the same move was followed by only +0.78% (t=1.21, n=218), and ordinary days above the SMA by +0.98%. Across all bars, 20-bar returns rose from +2.8% after |z|<1 days to +8.3% after z of 2–3 (n=368) and +11.3% after z>3 (n=193).

---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's past 20-day return is in the top part of its range, the coin's next 20 bars rise further than when its past 20-day return is low.
Consequence: A trader would size longs by recent 20-day momentum rather than by how far price sits from its long average.
Why:
- F8: Past 20-day return sorted the next returns more cleanly than the SMA distance did. From the lowest to the highest past-20-day quintile, the forward 20-bar return rose monotonically from +1.3% to +5.3%, and the next-day return from +0.11% to +0.32% (overlapping, pooled across coins).
- F1: When the close was above the 200-day SMA, a daily up-move larger than 2 standard deviations was followed by a mean 5-bar return of +3.39% (t=3.81, n=323, overlapping windows). Below the SMA the same move was followed by only +0.78% (t=1.21, n=218), and ordinary days above the SMA by +0.98%. Across all bars, 20-bar returns rose from +2.8% after |z|<1 days to +8.3% after z of 2–3 (n=368) and +11.3% after z>3 (n=193).

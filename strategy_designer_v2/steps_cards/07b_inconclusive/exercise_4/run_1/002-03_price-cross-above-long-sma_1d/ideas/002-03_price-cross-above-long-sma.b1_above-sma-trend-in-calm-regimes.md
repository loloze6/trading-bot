---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day simple moving average, the further above it sits relative to its own past distances, the more the coin outperforms its average return over the next 20 days, only while its 60-day volatility is low relative to its own past.
Consequence: A trader would follow price above the 200-day average mainly in calm stretches, and refuse to chase it when volatility is high.
Why:
- F6: Sizing by volatility is what lifts the measure. The plan's allocation-weighted main measure reaches t 1.73. The same cases with equal weights give only t 0.32. The allocation is volatility-targeted on 60-day volatility, so the effect leans toward the calmer stretches, where positions are larger.
- F1: The edge is too small to separate from noise at the plan's horizon. On the 399 non-overlapping 20-day cases above the 200-day SMA, the mean excess return over holding is 0.0052 (t 0.32), against -0.0002 on the 412 cases below it (Welch t 0.27).
- F5: The effect changes sign between coins and between periods.

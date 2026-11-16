---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 10-day return measured against its 20-day daily volatility, the larger its rise over the next 10 days.
Consequence: Above the long average, a trader would scale a long by the coin's recent volatility-adjusted 10-day gain rather than by its place in the 20-day range.
Why:
- F1: While the close is at or above its 200-day average, the coin's 10-day past return predicts its excess 10-day forward return better than the tested range position does. The pooled slope t is 4.40, with 761 grid cases. When both enter one regression on 698 cases, past 10-day return keeps t = 2.85 and the 20-day range position falls to t = 0.91.
- F2: In the same regime, the trend shows as a steady rise across past 10-day return quintiles, from -0.0226 in the lowest to +0.0263 in the highest (96 to 212 cases each). Below the 200-day average the slope disappears: t = -0.23 on 786 cases.
- F3: Scaling the 10-day return by the 20-day volatility strengthens this. In the trending regime the pooled t is 4.62. The slope is positive in all six coins, with t of 3.49 for XRP, 2.15 for ETH and 2.01 for ZEC.

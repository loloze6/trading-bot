---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits below its 200-day simple moving average and the more it has fallen over the past 30 days, the more it rises beyond its usual drift over the next 20 days.
Consequence: A trader would treat deep, fresh drops under the long average as rebound candidates rather than as short signals.
Why:
- F3: The test's grading runs against the effect. The deepest forecast quartile is followed by a rise, excess +0.0076 (t 0.71, n 211), while the shallow quartile falls, -0.0080 (t -0.84). The deepest distance bin (-72% to -36.5%) averages -0.0001 against -0.0068 for the shallowest bin. The slope of excess return on allocation is -0.0126, so the clipped standardised forecast puts its largest shorts where falls stop.
- F5: The coin's recent path splits the outcome. Below the SMA200, a high 30-day return (top quartile) is followed by excess -0.0159 over 10 days (t -1.55, n 154). The lowest 30-day return is followed by +0.0064 over 10 days and +0.0479 over 20 days (t 1.58, n 67): bounces under a falling average fail, and sharp drops rebound.

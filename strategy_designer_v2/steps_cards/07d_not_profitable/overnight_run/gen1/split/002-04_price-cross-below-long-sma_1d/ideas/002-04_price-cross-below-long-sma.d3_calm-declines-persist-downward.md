---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is below its 200-day average while the coin is calm and its 20-day trend is down, the coin keeps drifting lower. When the same situation comes with high volatility, the coin tends to rise.
Consequence: A trader should short below the long average only in calm declines and stand aside, or lean long, in volatile ones.
Why:
- F7: The losses sit in volatile falling markets: active bars with a negative 20-day trend lost -0.0043 per bar when volatile and -0.0018 when mid-volatility, while the calm ones earned +0.00049, and the coin rose +0.25% per day in the volatile ones.
- F4: Across all active bars the coin rose more while the book was short (+0.136% per day) than while it was flat (+0.120% per day), and a unit short over all active bars earns -0.00136 per day (t = -2.97), which is a reversal, not downward persistence.

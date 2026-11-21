---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The closer a coin's hourly close is to its highest close of the last 30 days, measured in units of its 30-day hourly volatility, the more it rises over the next 10 days above its usual 10-day return.
Consequence: A trader would favour ten-day longs in coins sitting within a small number of their own usual moves of the monthly high, and give less weight to coins further below it.
Why:
- F2: Nearness to the 30-day high carries a 10-day move the surge does not explain: on the grid starting at each window's first row, cells in each coin's top quintile of close over its 30-day highest close are followed by a 10-day excess return of +3.9 % (t 3.02, 278 cases), against -0.1 % to -3.0 % in the four lower quintiles; on the 5-day horizon the same top quintile gives +2.3 % (t 2.67).
- F3: The nearness effect is not robust to where the grid starts: on the grid shifted by 5 days, the same top quintile gives +1.5 % (t 1.35, 287 cases). The within-coin Spearman correlation of nearness with the 10-day excess is weak (-0.04 to +0.12, no p below 0.06), and earlier runs already found nearness to highs pays (findings F3, F9). F2 is therefore at best a modest, graded effect at the top end only.
- F6: Nearness scaled by the coin's 30-day volatility sorts like raw nearness. Its top quintile gives +4.0 % (t 3.05) on the first grid and +1.9 % (t 1.63) on the shifted grid, the most stable of the nearness measures across the two grids.
- F9: The moves in F2 and F4 are large against a trade: a 10-day excess of +3.9 % to +7.4 % per case is 20 to 39 times the 0.19 % round-trip cost of this backtest. Size is not the obstacle; robustness across grid offsets (F3) and years (F7) is.

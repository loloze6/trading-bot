---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days, except when its 30-day return is already extended, where the larger that 30-day return, the smaller the rise over the next 10 days.
Consequence: A trader would scale a long by how near the close is to its 20-day high above the long average, and cut it back as the coin's 30-day run grows very large, which is where the book's deepest falls start.
Why:
- F3: Dropping the shorts would fix most of the falls. In an approximate rebuild of the book, long-only cuts the deepest fall from -0.340 to -0.243 and lifts Calmar from 0.46 to 0.70 and mean daily return from 0.000468 to 0.000486. Also skipping longs whose 30-day return is in the top fifth cuts the fall to -0.195 and lifts Calmar to 0.89 and Sharpe to 1.08, with the mean at 0.000476.
- F4: The drift fades when the coin has already run far. Long bars whose past 30-day return is in the top fifth (above +44%) gain -0.000168 a day. The middle fifth (+15% to +28%) gains 0.004317. On the trending 10-bar grid, the 10-day forward return is +0.053 (t 2.95, n 126) for 30-day returns of +18% to +36%, but only +0.013 (t 0.67, n 126) for the top fifth.
- F5: The worst moves come after extended runs while long. The worst 2% of position-bars are 73% long and all in the trending regime. On those bars the past 30-day return averages +30%, the past 10-day return +13% and the range position 0.70.

---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days, the coin still rising, only less, when its close sits in the lower half of that range.
Consequence: A trader would hold only longs graded by range position above the long average, and refuse shorts near the range low, since those pay fees for a fall that does not come.
Why:
- F1: The short side earns nothing after fees. In the trending regime, short bars gain 0.000178 a day before fees and pay 0.000231 in fees, so they net -0.000053 over 3316 bars, while long bars net 0.001633 over 5173 bars (summed gain before fees 0.62 for shorts against 9.50 for longs).
- F2: The lower half of the 20-day range does not lead to a fall. On the trending 10-bar grid, bars with a negative forecast are followed by +0.0023 over 10 days (t 0.24, n 229), against +0.0274 (t 2.96, n 401) for bars with a positive forecast. Selling the low half bets on a fall that is not in the data.
- F3: Dropping the shorts would fix most of the falls. In an approximate rebuild of the book, long-only cuts the deepest fall from -0.340 to -0.243 and lifts Calmar from 0.46 to 0.70 and mean daily return from 0.000468 to 0.000486. Also skipping longs whose 30-day return is in the top fifth cuts the fall to -0.195 and lifts Calmar to 0.89 and Sharpe to 1.08, with the mean at 0.000476.

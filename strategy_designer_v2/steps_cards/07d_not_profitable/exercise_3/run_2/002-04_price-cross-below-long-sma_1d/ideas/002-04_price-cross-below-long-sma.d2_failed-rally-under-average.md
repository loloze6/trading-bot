---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits below its long moving average, the coin keeps falling, more the further it sits below, only after it has stopped falling over recent bars or rebounded towards the average: the stronger that recent rebound under the average, the larger the fall that follows.
Consequence: Short coins below the long average on rallies that fail under it rather than after fresh breakdowns, so the short avoids the rebound phase that carries the book's falls.
Why:
- F4: Shorts lose after a sharp, deep fall and gain after a pause or bounce under the average. In the most negative 20-bar momentum quartile (below -15%) the gain is -0.0047 with excess +0.46%; in the two highest quartiles it is +0.0055 (t 1.29) and +0.0032 (t 1.51). When the close is more than 34% under its 60-bar high the gain is -0.0065 with excess +1.57%; between 9% and 34% under it the gain is +0.0025 and +0.0091 (t 1.39).
- F2: The book's falls are rallies it was short into: its worst 5% of 20-day segments (41 cases) lost -14.8% on average while the coin rose +21.8%, and the coin was up in 92.7% of them; in its best segments the coin fell -17.0%.
- F3: The deepest forecasts carry the largest short and the worst result: at forecast -15 to -20 the mean allocation is -0.84, the mean gain is -0.0154 (t -1.32, n 125) and the coin's excess 10-bar return is +2.15%, a reversal. At forecast -5 to -15 the shorts gain +0.0048 (t 0.86, n 169) and +0.0028 (t 0.92, n 275).

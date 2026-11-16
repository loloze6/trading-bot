---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits below its long moving average, the coin keeps falling, more the further it sits below, except when the close has already fallen sharply and far beneath its recent high, where it rebounds more strongly the deeper and faster that fall was.
Consequence: Scale the short by depth below the long average only while the decline is orderly, and refuse or shrink it once the coin is stretched far and fast below its recent high, where the book's largest shorts met its rallies.
Why:
- F2: The book's falls are rallies it was short into: its worst 5% of 20-day segments (41 cases) lost -14.8% on average while the coin rose +21.8%, and the coin was up in 92.7% of them; in its best segments the coin fell -17.0%.
- F3: The deepest forecasts carry the largest short and the worst result: at forecast -15 to -20 the mean allocation is -0.84, the mean gain is -0.0154 (t -1.32, n 125) and the coin's excess 10-bar return is +2.15%, a reversal. At forecast -5 to -15 the shorts gain +0.0048 (t 0.86, n 169) and +0.0028 (t 0.92, n 275).
- F4: Shorts lose after a sharp, deep fall and gain after a pause or bounce under the average. In the most negative 20-bar momentum quartile (below -15%) the gain is -0.0047 with excess +0.46%; in the two highest quartiles it is +0.0055 (t 1.29) and +0.0032 (t 1.51). When the close is more than 34% under its 60-bar high the gain is -0.0065 with excess +1.57%; between 9% and 34% under it the gain is +0.0025 and +0.0091 (t 1.39).
- F1: The book loses its gain to the coin's drift and not to fees: it is short on 57.3% of bars, and on those bars the coin still rises +0.00115 a day, close to its pooled mean of +0.00129 and against +0.00147 on flat bars, so short bars earn -0.000444 a day; the whole book's gross gain is -0.000255 a day against fees of only -0.000026 a day.

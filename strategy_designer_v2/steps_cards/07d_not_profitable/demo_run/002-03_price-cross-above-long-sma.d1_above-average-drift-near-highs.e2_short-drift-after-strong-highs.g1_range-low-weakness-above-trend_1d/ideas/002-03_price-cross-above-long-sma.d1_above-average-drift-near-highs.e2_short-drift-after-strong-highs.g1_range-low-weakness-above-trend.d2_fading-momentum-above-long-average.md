---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the weaker its 60-day return, the larger its fall over the next 5 days.
Consequence: A trader would avoid or short a coin that holds above its long average while its 60-day momentum has gone flat or negative.
Why:
- F4: On the 5-day grid inside the up-trend, the coin's excess 5-day return falls as its 60-day return weakens: Spearman 0.157 between the 60-day return and the next 5-day return on short grid cases (p 0.0067, n 297). Among short cases, excess return is -0.0236 when the 60-day return is in its lowest third (n 143) and +0.0018 in its highest third (n 67).
- F5: When the 60-day return is at most 13 %, even closes in the middle of the 20-day range are followed by an excess 5-day return of -0.0256 (n 51). When the 60-day return is higher, those closes are followed by +0.0102 (n 190), so the 60-day return carries the fall at least as much as the range position does.

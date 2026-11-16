---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the nearer its close sits to the low of its 20-day closing range, the larger its fall over the next 5 days, only while its 60-day return is near or below zero, and the weaker that 60-day return, the larger the fall.
Consequence: A trader would short pullbacks to the range low in an up-trending coin only once its 60-day gain has faded, and would refuse that short after a strong 60-day rise.
Why:
- F1: Holding the short fights the coins' own rise. Every coin rose on average, from 0.00067 (LTC) to 0.00155 (ZEC) a day, so the short position's share of that drift costs -0.000103 a bar. That cost is about four times the book's whole gain before fees of 0.000025 a bar, and the book's mean daily return ends at -2.1e-05.
- F2: The short pays only when the coin's own 60-day return is at or below zero: 0.00242 a bar before fees, 0.00221 after (t 2.50, n 440 short bars). With a 60-day return of 0 to 13 % it earns nothing (0.00012, t 0.08, n 387). Above 13 % it loses -0.00060 (n 627) and -0.00045 (n 482). That losing group is 57 % of the short bars with a known 60-day return.
- F4: On the 5-day grid inside the up-trend, the coin's excess 5-day return falls as its 60-day return weakens: Spearman 0.157 between the 60-day return and the next 5-day return on short grid cases (p 0.0067, n 297). Among short cases, excess return is -0.0236 when the 60-day return is in its lowest third (n 143) and +0.0018 in its highest third (n 67).
- F5: When the 60-day return is at most 13 %, even closes in the middle of the 20-day range are followed by an excess 5-day return of -0.0256 (n 51). When the 60-day return is higher, those closes are followed by +0.0102 (n 190), so the 60-day return carries the fall at least as much as the range position does.

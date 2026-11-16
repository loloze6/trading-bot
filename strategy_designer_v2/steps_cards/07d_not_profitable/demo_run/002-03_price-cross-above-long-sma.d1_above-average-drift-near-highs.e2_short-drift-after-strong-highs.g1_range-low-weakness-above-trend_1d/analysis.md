---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3188 USD
---
## Findings
- **F1:** Holding the short fights the coins' own rise. Every coin rose on average, from 0.00067 (LTC) to 0.00155 (ZEC) a day, so the short position's share of that drift costs -0.000103 a bar. That cost is about four times the book's whole gain before fees of 0.000025 a bar, and the book's mean daily return ends at -2.1e-05.
- **F2:** The short pays only when the coin's own 60-day return is at or below zero: 0.00242 a bar before fees, 0.00221 after (t 2.50, n 440 short bars). With a 60-day return of 0 to 13 % it earns nothing (0.00012, t 0.08, n 387). Above 13 % it loses -0.00060 (n 627) and -0.00045 (n 482). That losing group is 57 % of the short bars with a known 60-day return.
- **F3:** Fees summed over all bars come to 0.83, against 0.43 of gross gain, which is 1.9 times the gain. The 2040 short trades average -0.41 % before fees and -0.51 % after.
- **F4:** On the 5-day grid inside the up-trend, the coin's excess 5-day return falls as its 60-day return weakens: Spearman 0.157 between the 60-day return and the next 5-day return on short grid cases (p 0.0067, n 297). Among short cases, excess return is -0.0236 when the 60-day return is in its lowest third (n 143) and +0.0018 in its highest third (n 67).
- **F5:** When the 60-day return is at most 13 %, even closes in the middle of the 20-day range are followed by an excess 5-day return of -0.0256 (n 51). When the 60-day return is higher, those closes are followed by +0.0102 (n 190), so the 60-day return carries the fall at least as much as the range position does.
- **F6:** The book's losses gather in a few windows. Its mean daily return is -0.00141 in w11, -0.00102 in w10 and -0.00072 in w22, against at most +0.00105 in its best window (w16).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend.d1_range-low-weakness-after-stalled-trend` (from F1, F2, F4, F5): While a coin's close is above its 200-day average, the nearer its close sits to the low of its 20-day closing range, the larger its fall over the next 5 days, only while its 60-day return is near or below zero, and the weaker that 60-day return, the larger the fall.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend.d2_fading-momentum-above-long-average` (from F4, F5): While a coin's close is above its 200-day average, the weaker its 60-day return, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

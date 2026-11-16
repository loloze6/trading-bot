---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3295 USD
---
## Findings
- **F1:** Inside the trending regime (close above its 200-day average), 5-day returns rise steadily with the close's place in its 20-day closing range, not only in the upper half the forecast uses: the pooled slope of the coin-demeaned 5-day return on range position is 0.0335 (t 3.65, n 1402 non-overlapping cases), and on the lower half alone it is 0.0756 (t 2.78, n 527), steeper than on the upper half (0.0317, t 1.17, n 875).
- **F2:** In the trending regime, closes in the bottom tenth of the 20-day range are followed by a demeaned 5-day return of -1.98% (t -2.39, n 150), and closes in the next band (0.1 to 0.25) by -1.46% (t -1.80, n 136). Below the middle of the range the forecast is clipped to 0, so the strategy holds no position there, while the top tenth gives +1.58% (t 2.23, n 368).
- **F3:** The weakness near the bottom of the range shows in every coin: all 6 coins have a negative demeaned 5-day return when the trending-regime range position is below 0.25, from -1.11% for BTC to -2.40% for XRP, each with t between -0.9 and -1.5 and n between 34 and 60 per coin.
- **F4:** That weakness is concentrated in the early years: -8.4% (t -3.95, n 35) in 2018 and -4.1% (t -2.19, n 29) in 2019, against about +0.2% to +0.4% (|t| < 0.4) in 2023 to 2025. It is real in the pooled sample but has faded in the recent windows.
- **F5:** The 20-day return makes the same point. In the trending regime its lowest per-coin quintile is followed by a demeaned 5-day return of -2.06% (t -3.09, n 284), and the other four quintiles all give +0.6% to +1.1%. Its slope among negative 20-day returns is 0.130 (t 2.95, n 481).
- **F6:** The book's gain comes from long holds while its many short ones lose. Trades lasting up to 1.5 days average -4.24% net (n 618) and those of 1.5 to 3 days average -1.90% (n 674), while trades of more than 15 days average +39.1% (n 397). Each daily coin's book mean stays below holding the coin (for example XMR -0.006% against +0.107% a day).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend` (from F1, F2, F3, F4): While a coin's close is above its 200-day average, the nearer its close sits to the low of its 20-day closing range, the larger its fall over the next 5 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g2_monthly-losers-keep-falling` (from F5, F1): While a coin's close is above its 200-day average, the more negative its 20-day return, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

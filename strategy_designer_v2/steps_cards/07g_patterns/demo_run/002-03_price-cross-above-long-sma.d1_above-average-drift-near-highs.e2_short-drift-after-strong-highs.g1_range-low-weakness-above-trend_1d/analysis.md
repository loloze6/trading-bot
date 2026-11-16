---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5292 USD
---
## Findings
- **F1:** The tested pattern exists only above the 200-day average. In the trending regime, grid bars with the close in the bottom fifth of its 20-day closing range had a mean excess 5-day return of -0.0196 (t -3.09, n 244), against +0.0108 (t 1.97, n 526) in the top fifth. Below the average there is no gradient: range position against excess 5-day return gives Spearman rho 0.003 (p 0.91, n 1441), against rho 0.063 (p 0.018, n 1402) in the trending regime.
- **F2:** The book loses because it is short a market that rises, not because the signal is wrong. On daily returns, the book earns -2.2e-05 per day. Its gain from the market's own rise is -1.03e-04 per day (mean position -0.087), so timing adds about +8.1e-05 per day. On the days it was short, the coin returned -0.00016 on average (n 3807), against +0.00157 on flat days (n 13573), so the shorted days were barely negative in raw terms.
- **F3:** The strongest signal bucket earns little once sized. Trending grid bars with forecast below -10 had a mean excess 5-day return of -0.0176 (n 279), but at a mean position of -0.68 the position-weighted 5-day gain was only +0.0019. The forecast-0 bars, where the book sits flat, carried +0.0066 mean excess (n 1032); the clip at 0 leaves that out.
- **F4:** Inside the trending regime, past strength also points the same way on the upper side. The 20-day return scaled by 20-day volatility rank-correlates with the excess 5-day return at rho 0.061 (p 0.022, n 1402), positive in 5 of 6 coins (ETH 0.100, XRP 0.104, ZEC 0.098, BTC 0.060). By raw 20-day-return quintile, the two weakest have excess -0.0262 (t -2.19) and -0.0134 (t -2.39), and the three strongest +0.0086 to +0.0109 (t about 1.6 each).
- **F5:** The trending-regime gradient is concentrated in the first half of the sample. For 2018–2021, the weakest volatility-scaled 20-day-return quintile had excess -0.0351 (t -3.09, n 143) and the other four +0.012 to +0.020. For 2022–2025 the weakest quintile was only -0.0063 (t -1.08) and there was no clear order. By year, the pooled excess 5-day return swings from -0.0230 (2018, t -3.42) to +0.0144 (2020, t 2.59) to -0.0137 (2022, t -2.88).
- **F6:** Coins' daily excess returns differ by weekday. Saturday averaged +0.00335 (t 4.08, n 2484), Thursday -0.00299 (t -2.70) and Tuesday -0.00242 (t -2.53). Saturday's t stands out even after looking at seven weekdays, but it is a fixed calendar condition and has not been split by coin or year.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend.g1_graded-momentum-above-long-average` (from F1, F2, F3, F4, F5): While a coin's close is above its 200-day average, the larger its 20-day return relative to its 20-day volatility, the larger its rise over the next 5 days: weak recent paths fall and strong recent paths keep climbing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

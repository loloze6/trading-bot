---
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3678 USD
---
## Findings
- **F1:** The book's gain is mostly the market's own rise taken part-time. Its daily beta to the coin is 0.18 (r² 0.25), it is in the market 44% of bars at a mean allocation of 0.19, and the alpha left is only 3.5 bps/day. It earned in the up years 2020 (gain 20.1 bps/bar on a 42.3 bps coin drift, 63% in market) and 2024 (12.5 bps on 24.4). It stayed out of 2022 (8% in market, coin −18.0 bps) and lost only 1.7 bps there.
- **F2:** The idea's own 20-bar horizon shows nothing. On the non-overlapping 20-bar grid, the excess return in the trending regime is +0.0023 (t 0.14, n 408) against −0.0022 (t −0.21, n 419) outside it. Forecast buckets are not monotone: +0.023, −0.052, −0.026 and +0.072 from low to high, with no |t| above 1.6.
- **F3:** The edge sits at the one-bar horizon and grows with the forecast. The next-bar coin return is 4.6 and 4.4 bps in the two lowest in-market forecast quintiles, 22.2 and 22.7 bps in the middle two, and 44.8 bps in the top quintile. There the position's gain is 49.3 bps per bar against 0.2 bps in the lowest (n ≈ 1,539 each).
- **F4:** Nearly all the gain came in moderate uptrends. Bars whose past 60-day rise lies in (0, 0.2] carry 49% of the summed gain and those in (0.2, 0.5] carry 48%. In the (0, 0.2] state, the next-bar return while in the market is 49.6 bps against 14.7 bps on all bars of that state. Bars after 60-day falls contribute −1.3% of the gain.
- **F5:** The gain is carried by a few trades. The top 5% of the 2,888 trades sum to 21,477 of the 26,441 total profit-percent points (81%). The win rate is 45% and the median trade is −0.78%.
- **F6:** It is not one coin's book, but three coins carry it. BTC, ETH and XRP earn about 10 bps/day (book Sharpe 1.19, 1.12 and 0.89), while LTC (−0.05 bps) and XMR (0.7 bps) earn nothing. The lowest leave-one-coin-out portfolio Sharpe is 0.77, with BTC left out.
- **F7:** The only 20-bar pocket inside the trending regime is the calm one. In the coin's lowest third of 30-day volatility, the excess 20-bar return is +0.041 (t 2.17, n 96). The middle third shows −0.023 (t −1.04, n 76) and the highest third −0.010 (t −0.32, n 96).
- **F8:** In-market bars are followed by a mean next-bar return of 19.7 bps against 5.7 bps for out-of-market bars (Welch t 1.85).

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-continuation-near-highs` (from F3, F2, F4): While a coin closes above its long moving average, its next-day return is larger the closer the close sits to its recent closing high and the stronger its recent rise. The continuation is short-lived, carried in the days right after the close.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_calm-uptrend-drift` (from F7, F4): A coin above its long moving average whose recent daily volatility is low relative to its own history drifts upward over the following weeks by more than its usual drift. The quieter the advance, the larger the drift.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e3_above-average-regime-carries-returns` (from F1, F8, F6): A coin's daily returns are higher while it closes above its long moving average than while it closes below it. The book's edge is mainly being exposed in that up regime and absent in sustained declines.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

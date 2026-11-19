---
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
idea tested: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3812 USD
---
## Findings
- **F1:** The 1-day reversal after a large 1-day fall is the strongest pattern found and the tested idea does not explain it: on a non-overlapping 24-hour grid, bars in each coin's lowest decile of past 24-hour return were followed by a next-day return of +0.94% above the coin's usual move (t = 5.64, n = 1713); the highest decile was followed by −0.35% (t = −2.19, n = 1713) and the ninth by −0.22% (t = −2.01); the middle deciles were all within |t| < 1.6.
- **F2:** The tested forecast does sort the 10-day outcome: after 10 days, the top forecast bin (15 to 20) shows +4.17% above the coin's mean (t = 2.62, n = 195) and the zero-forecast bars show −1.07% (t = −2.24, n = 853), on the non-overlapping 240-bar grid with 1674 cases in total. The middle bins rise in order: −0.96%, +0.35% and +1.22%.
- **F3:** A plain past 10-day return carries the same continuation: the top per-coin quintile of 10-day return was followed by +3.00% over the next 10 days (t = 2.50, n = 308), and the second and third quintiles by −2.15% (t = −2.87) and −2.04% (t = −2.64). The lowest quintile was only −0.72% (t = −0.87), so the grading holds from the middle upward and not at the bottom.
- **F4:** The book loses through turnover, not through a wrong signal: its gross position gain per day is positive on 5 of 6 coins (BTC +0.143%, ETH +0.155%, XRP +0.117%), but fees per day are larger on every coin (BTC 0.186%, ETH 0.158%, XMR 0.341%); there are 95,811 long trades averaging 14.4 hours, with +0.50% gross and +0.40% net per trade, at 5.45 trades per day.
- **F5:** Of BTC's gross gain of 0.143% per day, only 0.047% comes from the market's own rise (mean position 0.37 × mean bar return), so about two-thirds is timing.
- **F6:** Hourly returns show strong clock effects. Bars starting at 20:00 and 21:00 UTC have t = 6.75 and 5.66, and bars at 02:00 and 13:00 have t = −3.80. Fridays have t = 5.83 and Thursdays t = −3.22. These effects are not graded, so they give no idea here.
- **F7:** The volatility level sorts nothing: across the quintiles of 10-day realised volatility, the 10-day excess return lies between −0.65% and +0.34%, with every |t| ≤ 1.02.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g1_one-day-drop-rebound` (from F1): The further a coin's price has fallen over the past 24 hours, the more it rises above its usual move over the next 1 day.
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.g2_ten-day-return-continuation` (from F3, F2, F5): The higher a coin's 10-day return, the more its price rises above its usual move over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

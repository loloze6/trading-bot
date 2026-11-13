---
line: 7.d not profitable
backtest: N1-01_trend-with-rising-month_1d
idea tested: N1-01_trend-with-rising-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5319 USD
---
## Findings
- **F1:** The book fails on drawdown, not on fees. Calmar is 0.50, below the 0.75 required. Each coin's worst drawdown runs from -46% (BTC) to -70% (ZEC, XRP), and the mean drawdown per window is -23.7%. Over 2,285 trades, fees average 0.10% against a mean gross gain of 5.19%, and the total fees paid (234) are 2% of the total gross gain (11,857).
- **F2:** The forecast has no measurable edge at the 20-bar horizon. On active bars, the forward 20-bar excess return is +1.5% with t=0.63 over 251 non-overlapping cases, and the forecast>2.5 bucket gives +1.45% with t=0.59 over 242 cases. A larger forecast does not earn more: the four entry-forecast quartiles average a gross gain of 6.2%, 4.3%, 2.3% and 7.8% per trade.
- **F3:** The book is a lottery on a few long trends.
- **F4:** The edge sits where the 60-bar trend is also up.
- **F5:** Keeping only active days with a positive 60-bar return cuts the mean drawdown per window from -23.7% to -14.2%, while the annualised mean falls only from 0.38 to 0.29.
- **F6:** Volatile states add drawdown without adding drift.

## Ideas
- `N1-01_trend-with-rising-month.d1_established-trend-confirms-persistence` (from F2, F4, F5): A coin that closes above its 200-day average with a positive 20-bar return keeps rising faster than its own average over the next 20 bars mainly when its 60-bar return is also positive, that is, when the short rise belongs to an older, established up-trend.
- `N1-01_trend-with-rising-month.d2_calm-trends-persist-better` (from F1, F6): A coin above its rising long average drifts upward over the next 20 bars more when its recent 20-day volatility is low relative to its own history.
- `N1-01_trend-with-rising-month.d3_persistent-state-not-fresh-entry` (from F3, F2): A coin whose close has stayed above its 200-day average with a positive 20-bar return on most of the last 20 bars keeps rising over the next 20 bars, while a coin that has only just entered that state tends to fall back out of it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.b inconclusive
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
idea tested: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4700 USD
---
## Findings
- **F1:** The tested slope of 14-day excess return on the forecast is essentially zero at every horizon, with t = 1.17 at 3 days (n=5723), 0.31 at 7 days (n=2443), -0.30 at 14 days (n=1152) and -0.90 at 30 days (n=539), so no horizon other than the plan's shows the continuation either.
- **F2:** Across quintiles of the raw share at 14 days the excess return does not rise. The lowest-share quintile (raw -0.46) has the highest excess return, +2.0%, and the highest-share quintile (raw +0.43) has -0.6%; at 30 days the same quintiles show +3.0% and -3.3%.
- **F3:** The pooled zero is a mix of opposite signs. By year, the 14-day slope t is -3.27 in 2018, +2.04 in 2019, -2.67 in 2020 and +2.47 in 2025. By coin, XRP alone has t = -2.85, while the other five coins pooled give a positive but weak slope (t = +1.35, n=960).
- **F4:** When the coin's own 60-day return is negative, the slope on the raw share is clearly negative: t = -3.52 at 14 days (n=211) and t = -2.40 at 7 days (n=566). The same slope while the 60-day return is positive is weaker, at t = -1.40 (n=221).
- **F5:** The reversal inside 60-day downtrends holds in all six coins, with 14-day slopes of t -2.69 for BTC, -2.17 for ZEC, -1.68 for XMR, -1.08 for LTC, -1.00 for ETH and -0.86 for XRP. It holds without XRP (t = -3.51, n=177). It is strongest in 2018 (t -4.02), 2020 (t -2.87) and 2022 (t -2.94), and it turns positive in 2019 (t +1.54).
- **F6:** Inside 60-day downtrends the gain sits mostly in the deepest cases. The quartile with the smallest RSI-above share (raw -0.49, 30-day return -26%) earns +12.7% excess over the next 14 days, against -3.9%, -5.0% and -4.2% in the other three quartiles. Only 37.5% of the 14-day cases have a 60-day return inside their window (432 of 1152).

## Ideas
- `010-01_rsi-above-share-continuation.b1_rsi-share-more-coins.b1_downtrend-rsi-below-share-rebound` (from F2, F4, F5, F6): While a coin's own 60-day return is negative, the smaller the share of the past 30 days that its 14-day RSI has spent above 50, the higher the coin's return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

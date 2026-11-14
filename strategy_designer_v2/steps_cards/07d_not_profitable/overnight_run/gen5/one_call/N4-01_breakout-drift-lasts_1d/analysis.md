---
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
idea tested: N4-01_breakout-drift-lasts
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2774 USD
---
## Findings
- **F1:** Fees are not the cause: the book is long only with 3269 trades, a mean gross gain of 4.37% per trade (t 5.72 over 3269 trades) against a mean commission of 0.29%, so the net mean is still 4.27%. The failed check is Calmar at 0.44, driven by drawdowns: the worst window drawdown per coin ranges from -73% (BTC) to -86% (LTC), and the window-mean drawdown reaches -77% in w14.
- **F2:** The gains are lopsided by holding time. The 1705 trades held more than 15 days earn +12.0% gross each (sum of net +20336%). The 1563 trades held 15 days or less all lose on average: -9.1% for 1 day or less, -4.6% for 1.5 to 3.5 days, -4.4% for 3.5 to 7.5 days and -3.3% for 7.5 to 15 days (sum of net -6374%). Overall the median trade is -2.4% and only 41.7% of trades win.
- **F3:** A larger forecast earns more only on the next day, and not over ten days. The next-day return rises from -0.0002 in the lowest active forecast fifth to +0.0028 and +0.0025 in the top two. On non-overlapping 10-bar returns of active bars, the forecast buckets 0-8, 8-15 and 15-20 give +1.6%, -1.2% and +0.4% (t 0.76, -0.89, 0.28; n = 36, 58, 56). Over all 198 such cases the mean is -0.1% (t -0.11).
- **F4:** Position grows with the forecast to an average of 1.97 at forecast 20, against 0.35 at forecasts up to 5, so the book is near 2x long exactly where F3 shows no 10-bar edge. This leverage adds to the drawdowns in F1.
- **F5:** The edge sits in strong prior uptrends. On active bars, the mean daily P&L is +0.0065 in the top quartile of the 20-day return (above +17%) and +0.0026 in the next quartile. It is only +0.0003 and +0.0004 in the two quartiles where the 20-day return is below +3.8%. Bars whose 60-day return lies between -20% and 0 lose -0.0022 per day over 1561 bars.
- **F6:** Losses follow the falling market. The book's mean daily return is negative in 2018 (-0.0039) and 2022 (-0.0015), in step with the coins (-0.0035 and -0.0018). Losing windows such as w1, w3, w7, w9, w12 and w14 coincide with falling coins (coin returns -10% to -50%).

## Ideas
- `N4-01_breakout-drift-lasts.d1_breakouts-need-prior-momentum` (from F5, F2): A close at a new 20-day high is followed by a further rise over the next one to two weeks when the coin has already risen strongly over the prior 20 days, rather than when it reaches the top of a flat range.
- `N4-01_breakout-drift-lasts.d2_rebound-highs-fail-fast` (from F5, F2, F6): A close at a new 20-day high reached while the close is still below its level of 60 days earlier is followed by price falling back within the next week.
- `N4-01_breakout-drift-lasts.d3_drift-is-slow-not-graded` (from F3, F4, F2, F1): Once a new 20-day high has been made, the upward drift of the following weeks accrues evenly across the days of the hold and does not grow with how close the latest close is to the high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

---
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
idea tested: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3703 USD
---
## Findings
- **F1:** Failed breakouts were not followed by a fall overall. Over 5 days the unusual move in the short direction was -0.48 % per case (t -1.18, 619 cases), and the total move was -1.06 %. The book's 1265 trades lost 2.94 % on average before fees and 3.04 % after, with 29 % winners, so the book loses on direction before cost matters.
- **F2:** The volatility condition sorts the cases the way the idea says, but the book is diluted by the volatile ones. Over 5 days, cases in the calmest quartile of 20-day volatility (below about 2.6 % a day) had an unusual move of +0.87 % (t 1.64, 155 cases). Cases in the most volatile quartile had -2.39 % (t -2.12, 155 cases): there, failed breakouts recovered.
- **F3:** The calm-market effect grows with the horizon. Over 10 days the calmest quartile had an unusual move of +1.84 % (t 1.83, 118 cases) and a total move of +0.73 %, against +0.87 % and +0.31 % over 5 days. The most volatile quartile went to -5.76 % (t -2.33, 118 cases).
- **F4:** Only the calm, longer-horizon version clears the cost of a trade (0.19 %) with room to spare. The calm 5-day total move of +0.31 % is about 1.6 times the cost, and the calm 10-day total move of +0.73 % is about 3.8 times. The 5-day total move over all cases (-0.69 % in the verdict) is negative.
- **F5:** The forecast does not grade the cases, so the book cannot lean on the calm ones through its signal.
- **F6:** The losses cluster in volatile, rebounding stretches.
- **F7:** Even the calm cases are not consistent across coins, so the calm-market effect is still fragile. Calm-quartile cases were positive in BTC (+1.82 %, t 2.38, 55 cases), XMR (+1.61 %, 36 cases) and ZEC (+2.65 %, 10 cases). They were negative in ETH, LTC and XRP.

## Ideas
- `029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline.d1_calm-failed-breakout-ten-days` (from F2, F3, F4, F5, F7): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 10 days, only while the coin's 20-day volatility of daily returns is low, and the lower that volatility, the larger the fall.
- `029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline.d2_calm-failed-breakout-after-rise` (from F2, F3, F6): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 10 days, only while the coin's 20-day volatility of daily returns is low and its 60-day return is positive, and the lower that volatility, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

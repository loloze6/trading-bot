---
line: 7.d not profitable
backtest: 029-01_failed-breakout-depth-decline_1d
idea tested: 029-01_failed-breakout-depth-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.7062 USD
---
## Findings
- **F1:** The coin did not fall after a failed breakout: over 619 cases it rose, with a mean short-direction 5-day excess return of -0.48 % (t -1.18) and a total move of -1.06 %. The book's 1266 trades lost 2.75 % gross and 2.85 % net on average, with 28.9 % winners, so the loss is the signal's direction and not the 0.19 % cost of a trade.
- **F2:** The effect is graded by the breakout day's volume against its 20-day average, but it only points the right way at the low end. In the lowest volume tercile the short excess is +0.72 % (t 1.14, strength +0.079, 206 cases). In the middle tercile it is -0.87 % and in the highest -1.29 % (t -1.59, strength -0.108), with a Spearman correlation of -0.062 between volume ratio and short excess.
- **F3:** The effect is also graded by the coin's 20-day volatility. In the lowest-volatility tercile the short excess is +0.54 % (t 1.10) and the total move is about 0 %. In the highest tercile it is -1.46 % (t -1.59) and the total move is -2.08 %. Low volatility together with low breakout volume gives +1.85 % (t 2.05, 68 cases), about ten times the cost of a trade.
- **F4:** The tested grading by depth below the old high does not appear: the depth terciles give -0.27 %, -0.65 % and -0.52 %. Breakout size grades the wrong way: breakouts under 0.7 % give +0.23 %, and breakouts over 2.4 % give -1.02 % (t -1.22).
- **F5:** 39.7 % of failed breakouts are followed within 5 days by a close above the breakout bar's close. Those 246 cases cost the short 7.2 %, while the other 373 cases earn 3.95 %. The brief's own refutation, a second successful break, is common, and it decides the result.
- **F6:** The book's falls come from strong uptrends. Its worst windows are ZEC w24 (coin +1161 %, book -56 %), LTC w17 (coin +99 %, book -50 %) and ETH w17 (coin +55 %, book -38 %). Across windows the book's return correlates -0.40 with the coin's return. In 2020–2021 the book lost 0.149 % and 0.047 % a day while the coins gained about 0.42 % and 0.41 % a day.

## Ideas
- `029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls` (from F1, F2, F3, F5): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, only while the breakout day's volume was below its 20-day average, and the lower that volume against its average, the larger the fall.
- `029-01_failed-breakout-depth-decline.d2_quiet-market-failed-breakout-falls` (from F1, F3, F6): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, only while the coin's 20-day volatility of daily returns is low, and the lower that volatility, the larger the fall.
- `029-01_failed-breakout-depth-decline.d3_marginal-breakout-failure-falls` (from F1, F4, F5): When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, and the smaller the breakout close's margin above that old high, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

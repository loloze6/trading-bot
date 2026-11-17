---
line: 7.d not profitable
backtest: 010-06_rsi-below-share-reversal_1d
idea tested: 010-06_rsi-below-share-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3950 USD
---
## Findings
- **F1:** The book loses because its sign is wrong rather than because of costs: its gross daily gain is -0.00102 while fees take only about 0.00003 per bar, and the same positions reversed earn a Sharpe of +0.84 against the book's -0.84 and holding's +0.64, positive in 16 of 24 windows, with a leave-one-out Sharpe range of 0.71 to 0.96.
- **F2:** Most of the loss comes from going short while the coin's 60-day return was positive (the RSI below-share is low then): on those 1308 days the book's mean daily gain was -0.00255 and its timing -0.00157, while long days in falling markets (1141 days) also lost, at a timing of -0.00158.
- **F3:** The share of days with RSI below 50 is mostly a mirror of the past trend, correlating -0.80 with the 60-day return and -0.73 with the 30-day return, and the pooled slope of the next 14-day return on the forecast is -0.00118 (t -1.65, 373 cases), negative for both BTC (t -1.28) and ETH (t -1.09).
- **F4:** The reversal the idea bets on appears only when the coin's 60-day return is negative: there the slope of the coin-demeaned next 14-day return on the share is +0.234 (t 2.27, n 65), and the forecast's slope is +0.0047 (t 1.51, n 64), and on days the book was short in a falling market its timing was +0.00154 (194 days).
- **F5:** When the coin's 60-day return is positive the relation runs the other way, toward continuation: the share slope is -0.109 (t -1.42, n 79) and the forecast slope is -0.0042 (t -1.95, n 78).

## Ideas
- `010-06_rsi-below-share-reversal.d1_rsi-weakness-reverts-in-downtrends` (from F2, F3, F4): The larger the share of the past 30 days that a coin's 14-day RSI has spent below 50, the higher the coin's return over the next 14 days, only while the coin's 60-day return is negative.
- `010-06_rsi-below-share-reversal.d2_rsi-strength-persists-in-uptrends` (from F1, F2, F5): The larger the share of the past 30 days that a coin's 14-day RSI has spent above 50, the higher the coin's return over the next 14 days, while the coin's 60-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

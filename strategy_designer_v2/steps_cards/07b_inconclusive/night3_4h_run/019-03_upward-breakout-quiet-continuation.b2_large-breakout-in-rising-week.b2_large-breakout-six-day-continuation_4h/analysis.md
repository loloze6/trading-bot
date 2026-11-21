---
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3444 USD
---
## Findings
- **F1:** The tested effect points the way the idea predicts but falls short of the bar. On my own recount, 1641 cases give a mean unusual 36-bar move of +0.53 % (t 1.70), matching step 5's +0.51 % (t 1.68). That move is 2.6 times the 0.19 % cost of a trade, so size is not what keeps the result unclear.
- **F2:** The supporting check could not work as planned. 88 % of the cases sit at the forecast's cap of 20, and the median is 20, so the median split above against below has almost nothing above it. The idea's grading by break size was not really measured.
- **F3:** Measured from the prices, break size does grade the move at the top. By quartile of the break in 30-day mean ranges, the unusual 36-bar move is +0.22 %, −0.33 %, +0.60 % and +1.62 % (t 2.52, 413 cases, median break 1.35 ranges). Across all cases the rank correlation is only 0.038 (p 0.13).
- **F4:** The effect is drowned by the market's own regimes. By year, the mean unusual 36-bar move is +2.56 % in 2020 (t 3.39, 239 cases) and −2.56 % in 2022 (t −3.66, 201 cases); every other year lies between −0.13 % and +1.45 %.
- **F5:** The effect is mixed across coins. Every coin's mean unusual move is positive, but none reaches t 1.1: BTC +0.46 %, ETH +0.51 %, XRP +1.03 %, ZEC +1.10 %, LTC and XMR +0.07 %. On 6 coins the data is simply too thin for the pooled +0.5 %.
- **F6:** The move shows mostly where the 7-day rise is large next to the coin's own volatility. By quartile of the 7-day return divided by its 7-day volatility, the 36-bar unusual move is −0.29 %, +0.15 %, +0.73 % and +1.51 % (t 2.15, 415 cases). Over 72 bars it is −1.47 %, +0.60 %, +1.01 % and +2.99 % (t 2.45). Case by case, the rank correlation is still about zero (0.0002), so the grading lives in the tails.
- **F7:** The move keeps building past six days when the coin's 30-day return is also positive. On those 811 cases the unusual move is +0.81 % over 36 bars (t 1.87) and +2.12 % over 72 bars (t 2.78, 766 cases). Against a negative 30-day return it is +0.26 % and −0.51 %.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins` (from F1, F5): When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive, the coin rises over the next six days. The farther that close sits above the two-day high, measured in the coin's 30-day average four-hour range, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b2_breakout-graded-by-trend-strength` (from F6, F7, F3, F4): When a four-hour bar closes above the highest high of a coin's preceding two days, the coin rises over the next twelve days. The larger the coin's 7-day return, measured in its own 7-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.

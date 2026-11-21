---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two days, the coin rises over the next twelve days. The larger the coin's 7-day return, measured in its own 7-day volatility, the larger the rise.
Consequence: A trader would hold upward breaks for about twelve days, and hold most firmly those that come out of a week that rose strongly for that coin's volatility, where the move per case is many times the cost of a trade.
Why:
- F6: The move shows mostly where the 7-day rise is large next to the coin's own volatility. By quartile of the 7-day return divided by its 7-day volatility, the 36-bar unusual move is −0.29 %, +0.15 %, +0.73 % and +1.51 % (t 2.15, 415 cases). Over 72 bars it is −1.47 %, +0.60 %, +1.01 % and +2.99 % (t 2.45). Case by case, the rank correlation is still about zero (0.0002), so the grading lives in the tails.
- F7: The move keeps building past six days when the coin's 30-day return is also positive. On those 811 cases the unusual move is +0.81 % over 36 bars (t 1.87) and +2.12 % over 72 bars (t 2.78, 766 cases). Against a negative 30-day return it is +0.26 % and −0.51 %.
- F3: Measured from the prices, break size does grade the move at the top. By quartile of the break in 30-day mean ranges, the unusual 36-bar move is +0.22 %, −0.33 %, +0.60 % and +1.62 % (t 2.52, 413 cases, median break 1.35 ranges). Across all cases the rank correlation is only 0.038 (p 0.13).
- F4: The effect is drowned by the market's own regimes. By year, the mean unusual 36-bar move is +2.56 % in 2020 (t 3.39, 239 cases) and −2.56 % in 2022 (t −3.66, 201 cases); every other year lies between −0.13 % and +1.45 %.
